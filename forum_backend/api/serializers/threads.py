

from wsgiref.validate import validator

from api.serializers.users import UserSerializer
from django.shortcuts import get_object_or_404
from polls.choices import PollType
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, Serializer
from tags.models import Tag

from comments.models import Comment
from threads.choices import ThreadCategories
from threads.models import MainThread, SubThread


class ForumSerializer(Serializer):
    id = fields.IntegerField()
    user = UserSerializer()
    title = fields.CharField()
    category = fields.CharField()
    description = fields.CharField()
    admin = fields.BooleanField()
    active = fields.BooleanField()
    created_on = fields.DateTimeField()


class PossibilitySerializer(Serializer):
    id = fields.IntegerField()
    text = fields.CharField()


class PollSerializer(Serializer):
    id = fields.IntegerField()
    question = fields.CharField()
    poll_type = fields.ChoiceField(PollType.choices, default=PollType.SINGLE)
    created_on = fields.DateTimeField()
    possibility_set = PossibilitySerializer(many=True)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'created_on']


class MainThreadSerializer(ModelSerializer):
    """Serialize the MainThread model"""
    user = UserSerializer()
    # tags = TagSerializer(many=True)
    # poll = PollSerializer()

    class Meta:
        model = MainThread
        fields = ['id', 'title', 'description', 'category', 'active', 'modified_on', 'created_on', 'category', 'user']


class SubThreadSerializer(ModelSerializer):
    user = UserSerializer()
    mainthread = MainThreadSerializer()
    # tags = TagSerializer()

    class Meta:
        model = SubThread
        fields = ['mainthread', 'user', 'title', 'category',
                  'active', 'created_on', 'modified_on', 'tags']


class ValidateSubThreadSerializer(Serializer):
    thread = fields.IntegerField()
    title = fields.CharField()
    description = fields.CharField()
    tags = fields.ListField()

    def save(self, user, **kwargs):
        thread = get_object_or_404(MainThread, id=self.validated_data.get('thread'))
        subthread = thread.subthread_set.create(**self.validated_data)
        tags = [Tag(tag) for tag in self.validated_data.get('tags', [])]
        saved_tags = [tag.save() for tag in tags]
        subthread.tags.add(*saved_tags)


class ValidatePollPossibilities(Serializer):
    text = fields.CharField()
    
    
class ValidatePollDisplay(Serializer):
    public_votes = fields.BooleanField(default=True)
    show_results_without_voting = fields.BooleanField(default=True)
    
    
class ValidatePollClosing(Serializer):
    poll_closes = fields.BooleanField(default=True)
    closing_days = fields.IntegerField(default=7)
    
    
class ValidatePollSerializer(Serializer):
    question = fields.CharField()
    possibilities = ValidatePollPossibilities(many=True)
    choice_selection: fields.ChoiceField(['single'])
    choices_limit = fields.IntegerField(default=2, validators=[])
    allow_vote_change = fields.BooleanField(default=True)
    
    display = ValidatePollDisplay()
    closing = ValidatePollClosing()
    

class ValidateNewThread(Serializer):
    title = fields.CharField()
    content = fields.CharField()
    type = fields.ChoiceField(ThreadCategories.choices, default=ThreadCategories.GENERAL)
    watch = fields.BooleanField(default=True)
    tags = fields.ListField(required=False)
    add_poll = fields.BooleanField(default=False)
    
    poll = ValidatePollSerializer(required=False)

    def create(self, validated_data):
        data = validated_data.copy()
        add_poll = data.pop('add_poll')
        if add_poll:
            poll_attrs = data.pop('poll')

            instance = Poll.objects.create(**poll_attrs)
            instance.public_votes = poll_attrs['display']['public_votes']
            instance.show_results_without_voting = poll_attrs['display']['show_results_without_voting']
            instance.poll_closes = poll_attrs['closing']['poll_closes']
            instance.closing_days = poll_attrs['closing']['closing_days']
            instance.save()
            
            thread = instance.mainthread.create(**data)
        else:
            data.pop('poll')
            thread = MainThread.objects.create(**data)
        return MainThreadSerializer(instance=thread)
