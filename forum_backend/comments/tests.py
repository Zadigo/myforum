from comments import tasks
from django.test import override_settings
from comments.models import Comment
from django.urls import reverse
from forum_backend.mixins import AuthenticatedTestCase


class TestCommentsApi(AuthenticatedTestCase):
    fixtures = [
        'fixtures/users',
        'fixtures/forums',
        'fixtures/threads',
        'comments'
    ]

    def test_get_comment(self):
        comment = Comment.objects.first()
        path = reverse(
            'comments_api:get_update_delete_comment',
            args=[comment.id]
        )
        response = self.client.get(path)
        self.assertIn('id', response.json())

    def test_create_comment(self):
        path = reverse('comments_api:create')
        data = {
            'thread': 1,
            'content': 'Quick content',
            'content_delta': '[]',
            'content_html': '<p>Quick content</p>'
        }
        response = self.client.post(path, data=data)

        data = response.json()
        self.assertIn('id', data)

    def test_get_update_comment(self):
        path = reverse('comments_api:create')
        data = {
            'title': 'Updated comment'
        }
        response = self.client.post(path, data=data)

        data = response.json()
        self.assertIn('id', data)

    def test_bookmark_comment(self):
        comment = Comment.objects.first()
        path = reverse('comments_api:bookmark', args=[comment.id])
        data = {'id': comment.id}
        response = self.client.post(path, data=data)

        data = response.json()
        self.assertIn('id', data)

    def test_test_latest_comment(self):
        path = reverse('comments_api:latest_comments')
        response = self.client.get(path)
        for item in response.json():
            self.assertIn('id', item)


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
class TestTasks(AuthenticatedTestCase):
    fixtures = [
        'fixtures/users',
        'fixtures/forums',
        'fixtures/threads',
        'comments'
    ]

    def test_comment_analysis(self):
        comment = Comment.objects.first()
        comment.content = (
            "This is a complexe text that can be used "
            "to shoutout @testuser in order to send some "
            "interesting notifications"
        )
        comment.save()

        t = tasks.analyze_comment.apply((comment.id, comment.content))
        t.get()

        notifications = comment.user.notification_set.all()
        # self.assertTrue(notifications.exists())
