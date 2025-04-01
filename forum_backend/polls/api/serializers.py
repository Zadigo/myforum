from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import fields
from rest_framework.serializers import Serializer

from moderation.utils import moderate_text_validator
from polls.choices import PollType
from polls.models import Poll, Possibility


class PollPossibilitiesSerializer(Serializer):
    id = fields.IntegerField(read_only=True)
    text = fields.CharField(validators=[moderate_text_validator])


class PollSerializer(Serializer):
    """Serializer for the Poll model"""

    id = fields.IntegerField()
    question = fields.CharField()
    possibility_set = PollPossibilitiesSerializer(
        many=True,
        read_only=True
    )
    poll_type = fields.CharField()
    choices_limit = fields.IntegerField()
    allow_vote_change = fields.BooleanField()
    closes = fields.BooleanField()
    closing_date = fields.DateField()
    public = fields.BooleanField()
    voters_alone = fields.BooleanField()
    active = fields.BooleanField()
    created_on = fields.DateTimeField()


# Validators

class ValidatePollPossibilitySerializer(Serializer):
    text = fields.CharField()


class ValidatePollSerializer(Serializer):
    """Validator for creating a new poll"""

    question = fields.CharField()
    possibilities = ValidatePollPossibilitySerializer(many=True)
    choice_selection = fields.ChoiceField(
        PollType.choices,
        default=PollType.SINGLE
    )
    choices_limit = fields.IntegerField(default=1)
    allow_vote_change = fields.BooleanField(default=True)
    display = fields.JSONField()
    closing = fields.JSONField()


class ValidateAnswer(Serializer):
    answers = fields.ListField()

    def save(self, request, poll):
        answers = self.validated_data['answers']

        poll = get_object_or_404(Poll, thread__id=poll)
        possibilities = get_list_or_404(Possibility, id__in=answers)
        instance = poll.answer_set.create(user=request.user)
        instance.possibilities.add(*possibilities)
