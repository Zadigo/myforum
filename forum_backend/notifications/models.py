from django.contrib.auth import get_user_model
from django.db import models

from comments.models import Comment
from notifications.choices import NotificationTypes


class Notification(models.Model):
    """Represents a notification for an event
    that occured on the forum"""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationTypes.choices,
        default=NotificationTypes.FOLLOW
    )
    read = models.BooleanField(
        default=False
    )
    created_on = models.DateField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_on', '-pk']

    def __str__(self):
        return self.user.username
