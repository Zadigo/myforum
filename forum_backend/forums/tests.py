from comments import views
from comments.models import Comment
from django.test import Client, RequestFactory, TestCase
from rest_framework.test import APITestCase


class TestForumApi(APITestCase):
    fixtures = ['comments']

    def test_list_forums(self):
        pass

    def test_list_forum_threads_view(self):
        pass

    def test_follow_forum_view(self):
        pass
