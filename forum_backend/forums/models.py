from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from forums.choices import ForumCategories
from forums.validators import validate_title

# Forum -> Threads [Main -> Sub] -> Comments

USER_MODEL = get_user_model()


class Forum(models.Model):
    """A forum regroups a set of topics 
    called threads. Forums are generally
    created by admins but can also be user
    created"""

    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.CharField(
        max_length=100,
        validators=[validate_title]
    )
    category = models.CharField(
        max_length=50,
        choices=ForumCategories.choices,
        default=ForumCategories.GENERAL,
        help_text=_(
            "Used to regroup forums of "
            "a same category together"
        )
    )
    description = models.TextField(
        max_length=250,
        blank=True,
        null=True
    )
    admin = models.BooleanField(
        default=False,
        help_text=_(
            "Specifies whether the forum "
            "is for admin purposes"
        )
    )
    active = models.BooleanField(
        default=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_on']
        indexes = [
            models.Index(
                condition=Q(active=True),
                fields=['active'],
                name='active_forums'
            )
        ]
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_forum_name')
        ]

    def __str__(self):
        return self.title

    @cached_property
    def number_of_threads(self):
        return self.mainthread_set.count()
