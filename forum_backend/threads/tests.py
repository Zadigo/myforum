from django.urls import reverse
from threads.models import SubThread

from forum_backend.mixins import AuthenticatedTestCase


class TestThreadsApi(AuthenticatedTestCase):
    fixtures = [
        'fixtures/users',
        'fixtures/forums',
        'fixtures/threads'
    ]

    def test_get_comments(self):
        obj = SubThread.objects.first()
        path = reverse('threads_api:detail', args=[obj.id])
        response = self.client.get(path)
        print(response.content)

    def test_create(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_follow(self):
        pass
