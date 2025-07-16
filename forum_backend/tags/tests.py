from django.urls import reverse
from rest_framework.test import APITransactionTestCase
from tags.models import Tag


class TestTagsApi(APITransactionTestCase):
    fixtures = ['tags']

    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name='test', slug='test')

    def test_search(self):
        print(Tag.objects.all())
        response = self.client.get(reverse('api_tags:search'), {'q': 'Eugé'})
        self.assertEqual(response.status_code, 200)

        for item in response.json():
            with self.subTest(item=item):
                self.assertIn('name', item)
                self.assertIn('slug', item)
                self.assertIn('id', item)
