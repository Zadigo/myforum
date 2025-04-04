from django.urls import reverse
from rest_framework.test import APITestCase
from threads.models import MainThread


class TestForumApi(APITestCase):
    fixtures = ['fixtures/users', 'fixtures/forums', 'fixtures/threads']

    @property
    def _get_thread(self):
        return

    def test_list_forums(self):
        path = reverse('forums_api:forums')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, 'Request failed')

    def test_list_forum_threads(self):
        instance = MainThread.objects.first()
        path = reverse('forums_api:forum_threads', args=[instance.id])
        response = self.client.get(path)
        print(response.content)
        self.assertEqual(response.status_code, 200, 'Request failed')

    def test_follow_forum(self):
        # path = reverse('forums_api:follow')
        # response = self.client.get(path)
        # print(response.content)
        pass
