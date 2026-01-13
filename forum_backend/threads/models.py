from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from forums.models import Forum
from threads.choices import ThreadCategories
from threads.validators import validate_title
from threads.managers import MainThreadManager

# Forum -> Threads [Main -> Sub] -> Comments


class AbstractThread(models.Model):
    """A thread regroups a set of comments"""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )
    forum = models.ForeignKey(
        Forum,
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.CharField(
        max_length=100,
        validators=[validate_title]
    )
    description = models.TextField(
        max_length=250,
        blank=True,
        null=True
    )
    category = models.CharField(
        max_length=50,
        choices=ThreadCategories.choices,
        default=ThreadCategories.GENERAL_DISCUSSION
    )
    # tags = models.ManyToManyField(
    #     Tag,
    #     blank=True
    # )
    # conditions = models.JSONField(
    #     help_text=_("A set of conditions to be executed once "
    #                 "an event occurs in the forum"),
    #     blank=True
    # )
    # revive_thread = models.BooleanField(
    #     help_text=_("Action where the modified by date is changed in order "
    #                 "to have the thread reach the top seciton of the forum")
    # )
    publish_on = models.DateField(
        help_text=_("Publish the comment on a given specific date"),
        blank=True,
        null=True
    )
    pinned = models.BooleanField(
        default=False
    )
    highlighted = models.BooleanField(
        default=False
    )
    published = models.BooleanField(
        help_text=_("Indicates that a thread was published"),
        default=True
    )
    active = models.BooleanField(
        default=False
    )
    modified_on = models.DateTimeField(
        auto_now=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    objects = MainThreadManager()

    class Meta:
        abstract = True
        ordering = ['-modified_on']
        indexes = [
            models.Index(fields=['title'])
        ]

    @cached_property
    def number_of_comments(self):
        result = self.comment_set.aggregate(Count('id'))
        return result['id__count']

    @cached_property
    def is_dead(self):
        """When the last comment from the thread is
        greater than X, mark is as dead"""
        current_date = timezone.now()
        last_comment = self.comment_set.last()
        difference = (current_date - last_comment.created_on).days
        six_months = 30 * 6
        return difference > six_months

    @cached_property
    def raw_participants(self):
        """Returns the total list of participants
        including the authenticated user"""
        return self.comment_set.values('user__id', 'user__username')

    @cached_property
    def participants(self):
        """Returns a unique list of participants
        including the authenticated user"""
        ids = []
        items = []
        for participant in self.raw_participants:
            if participant['user__id'] not in ids:
                items.append(participant)
                ids.append(participant['user__id'])
                continue
        return items

    @property
    def latest_comment(self):
        try:
            # If there's no comment, this raises a "Comment matching
            # query does not exist" error. Technically a thread will
            # not be created without at least a first comment but
            # we'll protect against this error anyways
            latest_comment = self.comment_set.latest('created_on')
        except:
            return {'id': None, 'user__username': None, 'created_on': None}
        else:
            return dict([
                ('id', latest_comment.id),
                ('user__username', latest_comment.user.username),
                ('created_on', latest_comment.created_on)
            ])

    @property
    def is_new(self):
        """When a thread has been created less than
        fifteen minutes ago, mark it as new"""
        current_date = timezone.now()
        difference = (current_date - self.created_on).total_seconds()
        fifteen_minutes = 15 * 60
        return difference < fifteen_minutes

    @property
    def hot_topic(self):
        """When the total amount of comments in a thread
        passes the 200 line, mark it as a hot topic"""
        return self.comment_set.count() > 200

    def list_of_participants(self, request):
        """Returns the list of participants in a thread
        excluding the authenticated user"""
        participants = self.raw_participants.exclude(
            user__id__in=[request.user.id]
        )
        return participants.values_list('user__username', flat=True)


class MainThread(AbstractThread):
    """A main-thread regroups either comments or
    other sub-threads"""

    followers = models.ManyToManyField(
        get_user_model(),
        related_name='main_thread_followers',
        blank=True
    )

    def __str__(self):
        return f"MainThread: {self.title}"


class SubThread(AbstractThread):
    """A sub-thread is a child of a main thread the mainly
    regroup comments. It is attached to a main parent thread"""

    main_thread = models.ForeignKey(
        MainThread,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"SubThread: {self.title}"


@receiver(pre_save, sender=MainThread)
def run_conditions_for_main_thread(instance, **kwargs):
    pass


@receiver(pre_save, sender=SubThread)
def run_conditions_for_sub_thread(instance, **kwargs):
    pass
