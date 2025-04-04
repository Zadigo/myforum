import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.expressions import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from polls.choices import PollType


class Possibility(models.Model):
    poll = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=100)
    created_on = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('possibility')
        verbose_name_plural = ('possibilities')

    def __str__(self):
        # TODO: Use the name of the poll with
        # the given date
        return f"{self.created_on}-{self.text}"


class Poll(models.Model):
    thread = models.ForeignKey(
        'threads.MainThread',
        on_delete=models.CASCADE
    )
    question = models.CharField(
        max_length=100
    )
    poll_type = models.CharField(
        max_length=100,
        choices=PollType.choices,
        default=PollType.SINGLE
    )
    choices_limit = models.PositiveIntegerField(
        default=2,
        validators=[]
    )
    allow_vote_change = models.BooleanField(
        default=True
    )
    closes = models.BooleanField(
        default=True
    )
    closing_date = models.DateField(
        default=timezone.now,
        validators=[]
    )
    public = models.BooleanField(
        default=True,
        help_text=(
            "Determines whether the votes "
            "are visible by all"
        )
    )
    voters_alone = models.BooleanField(
        default=True,
        help_text=(
            "Determines whether the results "
            "are visible by voters alone"
        )
    )
    active = models.BooleanField(
        default=False
    )
    created_on = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = _('poll')
        indexes = [
            models.Index(fields=['question'])
        ]
        constraints = [
            UniqueConstraint(
                fields=['thread'],
                name='one_poll_per_thread'
            )
        ]

    def __str__(self):
        return self.question

    def clean(self):
        # The default closing date is 7 days
        # after the poll was created
        self.closing_date = datetime.timedelta(days=7) + self.closing_date


class Answer(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    possibilities = models.ManyToManyField(
        Possibility
    )
    created_on = models.DateField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('answer')

    def __str__(self):
        return str(self.created_on)
