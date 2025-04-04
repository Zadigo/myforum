from django.core.exceptions import ValidationError
from django.shortcuts import get_list_or_404
from django.utils import timezone
from polls.choices import PollType
from polls.models import Answer, Poll, Possibility
from rest_framework import fields
from rest_framework.serializers import Serializer, ModelSerializer, RelatedField, ReadOnlyField


class PollPossibilitiesSerializer(Serializer):
    id = fields.IntegerField(read_only=True)
    # TODO: Moderate poll possibilities
    text = fields.CharField()


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


class AnswerSerializer(ModelSerializer):
    user__username = ReadOnlyField(source='user.username')
    possibilities = PollPossibilitiesSerializer(many=True)

    class Meta:
        model = Answer
        fields = ['id', 'possibilities', 'user__username']


class ValidatePollPossibilitySerializer(Serializer):
    text = fields.CharField()

    def validate_text(self, value):
        # TODO: Schedule moderation via task
        return value


class ValidatePollSerializer(Serializer):
    """Validator for creating a new poll"""

    question = fields.CharField()
    possibilities = ValidatePollPossibilitySerializer(many=True)
    choice_selection = fields.ChoiceField(
        PollType.choices,
        default='Single'
    )
    choices_limit = fields.IntegerField(default=1)
    allow_vote_change = fields.BooleanField(default=True)
    display = fields.JSONField()
    closing = fields.JSONField()

    def validate_question(self, value):
        # TODO: Schedule moderation via task
        return value


class ValidateAnswer(Serializer):
    answers = fields.ListField(write_only=True)

    def create(self, validated_data):
        request = self._context['request']
        poll: Poll = self._context['poll']

        answer_ids = validated_data['answers']
        possibilities = get_list_or_404(
            Possibility,
            id__in=answer_ids,
            poll=poll
        )

        # 1.= Check that the poll is active
        if not poll.active:
            raise ValidationError('Poll is closed')

        # 2. Check that the poll allows vote change

        # 3. Check that the poll accepts only
        # one or multiple answers
        number_of_answers = len(validated_data['answers'])
        if poll.poll_type == 'Single':
            if number_of_answers > 1:
                raise ValidationError("Poll accepts only single answers")
        elif poll.poll_type == 'Multiple':
            if number_of_answers > poll.choices_limit:
                raise ValidationError(
                    f"Poll only accepts {poll.choices_limit} answers")

        # 4. Check that the poll closes and that the answer
        # respects the closing date
        d = timezone.now()
        if poll.closes:
            if d > poll.closing_date:
                raise ValidationError('Poll is closed')

        new_answer = poll.answer_set.create(user=request.user)
        new_answer.possibilities.add(*possibilities)
        return new_answer
