from comments.models import Comment
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from threads.models import MainThread

from forum_backend import utils

USER_MODEL = get_user_model()


class UserModerationPreference(models.Model):
    """A model that saves user's personal preferences
    in terms of moderation for the given thread"""

    user = models.ForeignKey(
        USER_MODEL,
        models.CASCADE,
        related_name='moderating_user'
    )
    user_to_moderate = models.ForeignKey(
        USER_MODEL,
        help_text=_("A user on which the moderation "
                    "preferences should be applied on"),
        on_delete=models.CASCADE,
        related_name='moderated_user'
    )
    mute_all = models.BooleanField(default=False)
    mute_posts = models.BooleanField(default=True)
    mute_threads = models.BooleanField(default=True)
    direct_messages = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'user_to_moderate'],
                name='one_auto_moderation_per_user'
            )
        ]

    def __str__(self):
        return str(self.user)


class Report(models.Model):
    """Reports made by users either on a thread, another
    user, a subthread or even a tag"""

    report_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    thread = models.ForeignKey(
        MainThread,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reporting_user',
        blank=True,
        null=True
    )

    reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='moderator',
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report: {self.report_id}'


@receiver(pre_save, sender=Report)
def create_report_id(instance, **kwargs):
    instance.report_id = utils.create_id('rep')
    admins = USER_MODEL.objects.filter(is_moderator=True)
    for admin in admins:
        pass
