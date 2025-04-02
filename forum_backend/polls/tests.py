from django.utils.http import parse_etags
from comments import views
from comments.models import Comment
from django.test import Client, RequestFactory, TestCase
from rest_framework.test import APITestCase


class TestPollsApi(APITestCase):
    fixtures = ['polls']

    def test_create(self):
        pass

    def test_get_poll(self):
        pass

    def test_get_poll_answers(self):
        parse_etags()
