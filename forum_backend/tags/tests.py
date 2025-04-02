from comments import views
from comments.models import Comment
from django.test import Client, RequestFactory, TestCase
from rest_framework.test import APITestCase


class TestTagsApi(APITestCase):
    fixtures = ['tags']

    def test_create(self):
        pass
