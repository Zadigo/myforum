from django.test import override_settings
from comments.models import SavedComment
from django.contrib.auth import get_user_model
from django.urls import reverse
from forums.models import Forum
from moderation.models import UserModerationPreference
from threads.models import MainThread, SubThread
import json
from forum_backend.mixins import AuthenticatedTestCase


class TestThreadsApi(AuthenticatedTestCase):
    fixtures = [
        'fixtures/users',
        'fixtures/forums',
        'fixtures/threads',
        'comments'
    ]

    def test_get_thread(self):
        obj = MainThread.objects.first()
        path = reverse('threads_api:detail_update', args=[obj.id])
        response = self.client.get(path)
        self.assertIn('id', response.json())

    def test_get_comments(self):
        obj = MainThread.objects.first()
        obj.comment_set.create(**{
            'title': 'Some title',
            'user': get_user_model().objects.first(),
            'thread': MainThread.objects.first(),
            'content': 'Some content'
        })
        path = reverse('threads_api:comments', args=[obj.id])
        response = self.client.get(path)
        self.assertIn('results', response.json())

    def test_get_comments_with_moderation_applied(self):
        obj = MainThread.objects.first()

        testuser2 = get_user_model().objects.create(**{
            'username': 'testuser2',
            'first_name': 'Pauline',
            'last_name': 'Parmentier',
            'email': 'pauline@gmail.com'
        })

        UserModerationPreference.objects.create(**{
            'user': self.user,
            'user_to_moderate': testuser2,
            'mute_all': True
        })

        obj.comment_set.create(**{
            'title': 'Some title',
            'user': testuser2,
            'thread': MainThread.objects.first(),
            'content': 'Some content'
        })

        path = reverse('threads_api:comments', args=[obj.id])
        response = self.client.get(path)
        self.assertIn('results', response.json())
        self.assertTrue(response.json()['count'] == 0)

    def test_get_comments_annotated_as_bookmarked(self):
        obj = MainThread.objects.first()

        comment = obj.comment_set.create(**{
            'title': 'Some title',
            'user': get_user_model().objects.first(),
            'thread': MainThread.objects.first(),
            'content': 'Some content'
        })

        SavedComment.objects.create(**{
            'user': self.user,
            'comment': comment
        })

        path = reverse('threads_api:comments', args=[obj.id])
        response = self.client.get(path)
        self.assertIn('results', response.json())

        for item in response.json()['results']:
            with self.subTest(item=item):
                self.assertTrue(item['bookmarked_by_user'])

    def test_create(self):
        path = reverse('threads_api:create')

        forum = Forum.objects.first()

        data = json.dumps({
            'forum_id': forum.id,
            'title': 'My title',
            'content': {
                'delta': 'Some delta',
                'html': '<p>Some html</p>',
                'text': 'Some text'
            },
            'category': 'General discussion',
            'watch': False,
            'result_thread_title': {},
            'schedule_date': None,
            'is_draft': False,
            'tags': ['One', 'Two', 'Three'],
            'add_poll': True,
            'poll': {
                'question': 'What are you?',
                'possibilities': [
                    {
                        'text': 'Possibility 1'
                    }
                ],
                'choice_selection': 'Single',
                'choices_limit': 1,
                'allow_vote_change': True,
                'display': {
                    'votes_publicly': True,
                    'results_without_voting': True
                },
                'closing': {
                    'days': 5,
                    'poll_closes': True
                }
            }
        })

        response = self.client.post(
            path,
            content_type='application/json',
            data=data
        )
        print(response.content)
        # self.assertIn('id', response.json())

    def test_update(self):
        instance = MainThread.objects.first()
        path = reverse('threads_api:detail_update', args=[instance.id])

        data = json.dumps({
            'title': 'My title'
        })

        response = self.client.patch(
            path,
            content_type='application/json',
            data=data
        )
        print(response.content)

    def test_delete(self):
        instance = MainThread.objects.create(title='Some title')
        path = reverse('threads_api:delete', args=[instance.id])
        response = self.client.delete(path)
        print(response.content)

    def test_follow(self):
        obj = MainThread.objects.first()
        path = reverse('threads_api:follow', args=[obj.id])
        response = self.client.post(path)
        self.assertIn('number_of_followers', response.json())


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
class TestTasks(AuthenticatedTestCase):
    pass
