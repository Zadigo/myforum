from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from polls.models import Answer, Poll, Possibility

from forum_backend.mixins import AuthenticatedTestCase


class TestPollsApi(AuthenticatedTestCase):
    fixtures = ['fixtures/users', 'fixtures/threads', 'polls']

    @property
    def _get_poll(self):
        return Poll.objects.first()

    def test_get_poll(self):
        path = reverse('polls_api:poll', args=[self._get_poll.id])
        response = self.client.get(path)
        self.assertIn('id', response.json())

        for item in response.json()['possibility_set']:
            with self.subTest(item=item):
                self.assertIn('id', item)

    def test_answer_poll(self):
        path = reverse('polls_api:answer_poll', args=[self._get_poll.id])
        data = {
            'poll': self._get_poll.id,
            'user': self.user.id,
            'answers': [1]  # One if single, multiple ids if Multiple
        }
        response = self.client.post(path, data=data)
        self.assertEqual(response.status_code, 200)

    def test_answer_poll_invalidity(self):
        path = reverse('polls_api:answer_poll', args=[self._get_poll.id])

        data = {
            'poll': self._get_poll.id,
            'user': self.user.id,
            'answers': [1]
        }

        # Cannot submit invalid amount of answers
        data['answers'] = [1, 2]
        with self.assertRaises(ValidationError):
            self.client.post(path, data=data)

        # Cannot submit none existing posibilities
        data['answers'] = [4]
        response = self.client.post(path, data=data)
        self.assertEqual(response.status_code, 404)

        # Cannot submit to an inactive poll
        poll = self._get_poll
        poll.active = ~F('active')
        poll.save()

        data['answers'] = [1, 2]
        with self.assertRaises(ValidationError):
            self.client.post(path, data=data)

        poll.active = ~F('active')
        poll.save()

        with self.assertRaises(ValidationError):
            self.client.post(path, data=data)

        # Cannot submit to a poll that is outdated
        poll.closing_date = timezone.now() - timedelta(days=50)
        poll.save()

        with self.assertRaises(ValidationError):
            self.client.post(path, data=data)

    def test_get_poll_answers(self):
        possibility = Possibility.objects.first()

        params = {
            'poll': self._get_poll,
            'user': self.user
        }
        answer = Answer.objects.create(**params)
        answer.possibilities.add(possibility)
        answer.save()

        path = reverse('polls_api:answers', args=[self._get_poll.id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertIn('user__username', response.json())

        for item in response.json():
            with self.subTest(item=item):
                self.assertIn('possibilities', item)
