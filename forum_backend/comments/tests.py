from django.test import TestCase, Client, RequestFactory

from comments.models import Comment
from comments import views

class TestComments(TestCase):
    fixtures = ['comments']

    def test_whats_new(self):
        factory = Client()
        response = factory.get('/api/v1/comments/whats-new', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
