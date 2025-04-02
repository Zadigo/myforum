from comments import views
from comments.models import Comment
from django.test import Client, RequestFactory, TestCase
from rest_framework.test import APITestCase


class TestCommentsApi(APITestCase):
    fixtures = ['comments']

    def test_create(self):
        pass
