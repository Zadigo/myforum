import datetime

from accounts.serializers import UserSerializer
from comments import tasks as comments_tasks
from django.shortcuts import get_object_or_404
from django.utils import timezone
from forums.api.serializers import ForumSerializer
from forums.models import Forum
from polls.api.serializers import PollSerializer, ValidatePollSerializer
from polls.models import Poll, Possibility
from rest_framework import fields
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import Serializer
from threads.choices import ThreadCategories
from threads.models import MainThread


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 30

    def get_paginated_response(self, data, **kwargs):
        response = super().get_paginated_response(data)
        response.data['pages'] = self.page.paginator.num_pages
        response.data = response.data | kwargs
        return response


class ThreadSerializer(Serializer):
    """A serializer for a thread that was
    created by a user - MainThread model"""

    id = fields.IntegerField()
    forum = ForumSerializer()
    user = UserSerializer()
    number_of_comments = fields.IntegerField()
    latest_comment = fields.JSONField()
    title = fields.CharField()
    category = fields.ChoiceField(
        ThreadCategories.choices,
        default='General discussions'
    )
    description = fields.CharField()
    owned_by_user = fields.BooleanField(default=False)
    participants = fields.ListField()
    active = fields.BooleanField(default=True)
    modified_on = fields.DateTimeField()
    created_on = fields.DateTimeField()

    def update(self, instance, validated_data):
        skip_keys = [
            'id', 'owned_by_user', 'participants', 'forum',
            'modified_on', 'created_on', 'owned_by_user',
            'number_of_comments', 'latest_comment'
        ]

        for key, value in validated_data.items():
            if key in skip_keys:
                continue
            setattr(instance, key, value)
        instance.save()
        return instance


class ValidateMainPostSerializer(Serializer):
    """Validates an incoming comment for
    a given thread"""

    delta = fields.JSONField()
    html = fields.CharField()
    text = fields.CharField()


class ValidateMainThreadSerializer(Serializer):
    """Validates the data for creating a new
    thread in the database given a forum ID"""

    forum_id = fields.CharField(write_only=True)
    title = fields.CharField()
    content = ValidateMainPostSerializer(write_only=True)
    result_thread_title = fields.JSONField(write_only=True)
    category = fields.ChoiceField(
        ThreadCategories.choices,
        default='General discussion'
    )
    watch = fields.BooleanField(default=True)
    tags = fields.ListField(write_only=True)
    schedule_date = fields.DateField(
        format='%Y-%m-%d',
        allow_null=True
    )
    is_draft = fields.BooleanField(default=False)
    add_poll = fields.BooleanField(default=False)
    poll = ValidatePollSerializer(allow_null=True)

    def validate_title(self, text):
        return text

    def validate(self, attrs):
        poll = attrs.get('poll', None)
        if poll is not None:
            number_of_possibilities = len(attrs['poll']['possibilities'])
            if attrs['poll']['choices_limit'] > number_of_possibilities:
                raise ValidationError(
                    details={
                        'choices_limit': 'Cannot be greater than the number of possibilities'
                    }
                )

            if attrs['add_poll'] and attrs['poll'] is None:
                raise ValidationError(detail={'poll': 'Poll cannot be None'})
        return attrs

    def create(self, validated_data):
        request = self._context['request']
        forum = get_object_or_404(Forum, id=validated_data['forum_id'])

        if not forum.active:
            raise PermissionDenied(detail='Forum is not active')

        thread = MainThread.objects.create(
            user=request.user,
            title=validated_data['title'],
            category=validated_data['category'],
            forum=forum
        )

        comment = thread.comment_set.create(
            user=request.user,
            content=validated_data['content']['text'],
            content_delta=validated_data['content']['delta'],
            content_html=validated_data['content']['html']
        )

        comments_tasks.analyze_comment.apply_async(
            args=[
                comment.id, 
                comment.content
            ],
            link=[
                comments_tasks.moderate_comment.s(comment.id)
            ],
            countdown=30
        )

        if validated_data['add_poll']:
            if validated_data['poll'] is None:
                raise ValidationError(detail={'poll': 'No poll data'})

            closing_days = validated_data['poll']['closing']['days']
            closing_date = timezone.now() + datetime.timedelta(days=closing_days)

            poll = Poll.objects.create(
                thread=thread,
                question=validated_data['poll']['question'],
                poll_type=validated_data['poll']['choice_selection'],
                choices_limit=validated_data['poll']['choices_limit'],
                allow_vote_change=validated_data['poll']['allow_vote_change'],
                closes=validated_data['poll']['closing']['poll_closes'],
                closing_date=closing_date,
                public=validated_data['poll']['display']['votes_publicly'],
                voters_alone=validated_data['poll']['display']['results_without_voting']
            )

            possibilities = [
                Possibility(poll=poll, text=item['text'])
                for item in validated_data['poll']['possibilities']
            ]
            possibilities_objs = Possibility.objects.bulk_create(possibilities)
            poll.possibility_set.add(*possibilities_objs)

        if not validated_data['is_draft']:
            thread.active = True
            thread.save()
        return thread
