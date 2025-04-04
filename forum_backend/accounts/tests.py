from forum_backend.mixins import AuthenticatedTestCase
from django.urls import reverse


class TestProfileApi(AuthenticatedTestCase):
    fixtures = ['fixtures/users']

    def test_get_profile(self):
        path = reverse('accounts_api:profile')
        response = self.client.get(path)
        print(response.content)
