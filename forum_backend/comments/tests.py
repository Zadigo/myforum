from comments import views
from comments.models import Comment
from django.test import Client, RequestFactory, TestCase
from rest_framework.test import APITestCase


class TestCommentsApi(APITestCase):
    fixtures = ['comments']

    def test_create_comment(self):
        pass

    def test_get_update_comment(self):
        pass

    def test_bookmark_comment(self):
        pass

    def test_test_latest_comment(self):
        pass

    def test_whats_new(self):
        pass
