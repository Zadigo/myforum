from comments import views
from comments.models import Comment
from django.test import Client, RequestFactory, TestCase


class TestThreadsApi(TestCase):
    fixtures = ['threads']

    def test_get_comments(self):
        pass

    def test_create(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_follow(self):
        pass
