from accounts.choices import StrikeChoices, StrikeReasonsChoices
from accounts.validators import ban_days_validator
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):
    """A custom user for the forum"""

    is_moderator = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('my user')

    def has_perm(self, perm, obj=None):
        initial_permission = super().has_perm(perm, obj=obj)
        # Query the databases to check if user is not on the
        # temporary or permanent ban lists
        # temp_banned_users = self.temporaryban_set.filter(user__email=self.email)
        # permanent_banned_users = self.permanentban_set.filter(user__email=self.email)

        logic = [
            initial_permission
            # True if not temp_banned_users.exists() else False,
            # True if not permanent_banned_users.exists() else False
        ]

        return all(logic)


class UserProfile(models.Model):
    """Represents the profile for a given user"""

    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE
    )
    preferred_topics = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    blocked_users = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        validators=[validate_comma_separated_integer_list]
    )
    followers = models.ManyToManyField(
        MyUser,
        related_name='followers',
        symmetrical=False,
        blank=True
    )
    forum_subscriptions = models.ManyToManyField(
        'forums.Forum',
        blank=True
    )
    thread_subscriptions = models.ManyToManyField(
        'threads.MainThread',
        blank=True
    )
    is_premium = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('user profile')

    def __str__(self):
        return self.user.username

    @cached_property
    def number_of_followers(self):
        return self.followers.all().count()


class AbstractBannedUser(models.Model):
    """Base models for banned users"""

    user = models.ForeignKey(
        MyUser,
        on_delete=models.DO_NOTHING
    )
    category = models.CharField(
        max_length=100,
        choices=StrikeChoices.choices,
        default=StrikeChoices.LEVEL1
    )
    reason = models.CharField(
        max_length=100,
        choices=StrikeReasonsChoices.choices,
        default=StrikeReasonsChoices.RACISM
    )
    appealed = models.BooleanField(
        default=False
    )
    appeal_reason = models.TextField(
        help_text=_("Reason invoked by the user to lift the ban")
    )
    apply_ban_on = models.DateTimeField(
        help_text=_("Ban a user on a specific date"),
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_on']
        abstract = True


class TemporaryBan(AbstractBannedUser):
    """Users who have been temporarily banned
    from the forum"""

    number_of_days = models.PositiveIntegerField(
        validators=[ban_days_validator]
    )
    start_date = models.DateTimeField(
        default=timezone.now
    )
    end_date = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        verbose_name = _('temporary ban')

    def __str__(self):
        return f'TemporaryBan: {self.user}'

    @property
    def is_banned(self):
        current_date = timezone.now()
        return self.start_date > current_date < self.end_date

    def clean(self):
        if self.number_of_days > 0:
            days = self.start_date.timedelta(days=self.number_of_days)
            self.end_date = days + self.start_date


class PermanentBan(AbstractBannedUser):
    """Users who have been permanently banned
    from the forum"""

    class Meta:
        verbose_name = _('permanent ban')

    def __str__(self):
        return f'TemporaryBan: {self.user}'


@receiver(post_save, sender=MyUser)
def create_user_profile(instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
