from django.db.utils import IntegrityError
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils import timezone
from moderation.utils import moderate_text_validator
from rest_framework import fields
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.validators import ValidationError
from threads.models import MainThread

from polls.choices import PollType
from polls.models import Poll, Possibility
from polls.validators import validate_possibility


class PollPossibilitiesSerializer(Serializer):
    id = fields.IntegerField(read_only=True)
    text = fields.CharField(validators=[moderate_text_validator])


class PollSerializer(Serializer):
    id = fields.IntegerField()
    question = fields.CharField()
    possibility_set = PollPossibilitiesSerializer(many=True, read_only=True)
    poll_type = fields.CharField()
    choices_limit = fields.IntegerField()
    allow_vote_change = fields.BooleanField()
    closes = fields.BooleanField()
    closing_date = fields.DateField()
    public = fields.BooleanField()
    voters_alone = fields.BooleanField()
    active = fields.BooleanField()
    created_on = fields.DateTimeField()
    
    
class ValidatePollSerializer(Serializer):
    thread = fields.IntegerField()
    question = fields.CharField(
        max_length=100,
        validators=[moderate_text_validator]
    )
    possibilities = PollPossibilitiesSerializer(
        many=True,
        validators=[validate_possibility]
    )
    poll_type = fields.ChoiceField(
        PollType.choices,
        default=PollType.SINGLE
    )
    choices_limit = fields.IntegerField(
        default=2, 
        validators=[]
    )

    allow_vote_change = fields.BooleanField(default=True)
    closes = fields.BooleanField(default=True)
    closing_date = fields.DateField(default=timezone.now)
    
    public = fields.BooleanField(default=True)
    voters_alone = fields.BooleanField(default=True)
    active = fields.BooleanField(default=False)
    
    created_on = fields.DateTimeField(required=False)
    
    def get_response(self):
        return Response(self.validated_data)

    def save(self, request, **kwargs):
        instance = get_object_or_404(MainThread, id=self.validated_data['thread'])
        data = self.validated_data.copy()
        
        possibilities = data.pop('possibilities')
        
        if len(possibilities) <= 1:
            raise ValidationError(detail='Needs at least one possibility')
        
        if len(possibilities) > 10:
            raise ValidationError(detail='Only a maximum of 10 possibilities are allowd', code=400)
        
        try:
            poll = instance.poll_set.create(**data)
        except IntegrityError:
            raise ValidationError(detail='Poll already exists')
        
        def func(x): return Possibility(poll=poll, **x)
        possibilities = map(func, possibilities)
                
        Possibility.objects.bulk_create(possibilities)
        



class ValidateAnswer(Serializer):
    answers = fields.ListField()
    
    def save(self, request, poll):
        answers = self.validated_data['answers']
        
        poll = get_object_or_404(Poll, thread__id=poll)
        possibilities = get_list_or_404(Possibility, id__in=answers)
        instance = poll.answer_set.create(user=request.user)
        instance.possibilities.add(*possibilities)
