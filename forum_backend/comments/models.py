from comments.utils import (files_upload_path, images_upload_path,
                            videos_upload_path)
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import ExpressionWrapper, F, Q
from django.db.models.functions import Now
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToCover
from notifications.choices import NotificationTypes
from tags.models import Tag
from threads.models import MainThread, SubThread

from forum_backend import utils

USER_MODEL = get_user_model()


class MediaContent(models.Model):
    """Contains different media contained for
    a specific givent comment. Media could be images
    videos, files etc."""

    media_content_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to=images_upload_path,
        blank=True,
        null=True
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToCover(300, 300)],
        format='JPEG'
    )
    file = models.FileField(
        upload_to=files_upload_path,
        blank=True,
        null=True
    )
    video = models.FileField(
        upload_to=videos_upload_path,
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.reference


class Quote(models.Model):
    """Represents a quote of a
    particular comment"""

    comment = models.ForeignKey(
        'Comment',
        models.CASCADE,
        help_text=_("The comment asking for the quote"),
        blank=True,
        null=True
    )
    quoted_comment = models.ForeignKey(
        'Comment',
        models.CASCADE,
        related_name='quoted_omment',
        help_text=_("The comment that is being quoted"),
        blank=True,
        null=True
    )
    content = models.TextField(
        help_text=_("The actual text of the quoted comment"),
        max_length=3000,
        blank=True,
        null=True
    )
    content_html = models.TextField(
        help_text=_(
            "The HTML representation of the quoted "
            "comment to be displayed on the page"
        ),
        max_length=6000,
        blank=True,
        null=True
    )
    modified_on = models.DateTimeField(
        auto_now=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'Quote: {self.quoted_comment.id}:: {self.comment.id}'


class Comment(models.Model):
    """Represents a comment in
    a givent thread"""

    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE
    )
    thread = models.ForeignKey(
        MainThread,
        on_delete=models.CASCADE
    )
    subthread = models.ForeignKey(
        SubThread,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    content = models.TextField(
        help_text=_("The actual text of the comment"),
        max_length=3000,
    )
    content_delta = models.JSONField(
        help_text=_(
            "The comment's text as "
            "Quill delta content"
        ),
        blank=True,
        null=True,
    )
    content_html = models.TextField(
        help_text=_(
            "The HTML representation of the "
            "text to be displayed on the page"
        ),
        max_length=6000,
        blank=True,
        null=True
    )
    media_contents = models.ManyToManyField(
        MediaContent,
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True
    )
    active = models.BooleanField(
        default=True)

    pinned = models.BooleanField(
        default=False
    )
    original_post = models.BooleanField(
        default=False
    )
    publish_on = models.DateField(
        help_text=_("Publish the comment on a given specific date"),
        blank=True,
        null=True
    )
    published = models.BooleanField(
        help_text=_("Indicates that a comment was published"),
        default=True
    )
    # ghost_readers = models.ManyToManyField(
    #     USER_MODEL,
    #     related_name='comment_gost_readers',
    #     blank=True
    # )
    # is_ghost_comment = models.BooleanField(
    #     default=False,
    #     help_text=_("A comment visible to only a specific set of users")
    # )
    # initial_comment = models.BooleanField(
    #     default=False
    # )
    modified_on = models.DateTimeField(
        auto_now=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_on', 'pk']
        indexes = [
            models.Index(
                fields=['created_on'],
                condition=Q(
                    created_on__gte=F('created_on') - 15
                ),
                name='last_fifteen_days_comments'
            ),
            models.Index(
                fields=['created_on'],
                condition=Q(
                    created_on__gte=F('created_on') - 7
                ),
                name='last_seven_days_comments'
            )
        ]

    def __str__(self):
        return f'Comment: {self.user}: {self.pk}'

    @cached_property
    def comment_length(self):
        pass


class SavedComment(models.Model):
    """Represents a bookmarked comment"""

    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'SavedComment: {self.comment}'


@receiver(pre_save, sender=MediaContent)
def create_media_content_id(instance, **kwargs):
    instance.media_content_id = utils.create_id('mc')


# @receiver(post_save, sender=Comment)
# def send_notifications(instance, created, **kwargs):
#     if created:
#         from notifications.models import Notification
#         followers = instance.thread.follower_set.all()
#         notifications = []
#         for follower in followers:
#             notification = Notification(
#                 user=follower,
#                 message=instance,
#                 notification_type=NotificationTypes.MESSAGE
#             )
#             notifications.append(notification)
