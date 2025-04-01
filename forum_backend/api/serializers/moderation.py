from django.db.models import query
from rest_framework.serializers import ModelSerializer, Serializer
from moderation.models import PersonalModeration
from django.contrib.auth import get_user_model
from rest_framework import fields

USER_MODEL = get_user_model()

class PersonalModerationSerializer(Serializer):
    user_to_moderate = fields.IntegerField()
    mute_all = fields.BooleanField(default=False)
    mute_posts = fields.BooleanField(default=True)
    mute_threads = fields.BooleanField(default=True)
    direct_messages = fields.BooleanField(default=True)

    def _get_users(self, user):
        ids = [user.id, self.validated_data.get('user_to_moderate')]
        return USER_MODEL.objects.filter(id__in=ids)

    def save(self, user, user_to_moderate, **kwargs):
        validated_data = self.validated_data | kwargs

        if self.instance is not None:
            self.instance = self.update(user, validated_data)
        else:
            self.instance = self.create(user, validated_data)
        
        if self.instance is None:
            raise ValueError()
        return self.instance

    def create(self, user, validated_data):
        users = self._get_users(user)
        PersonalModeration.objects.create(
            user=users[0], 
            user_to_moderate=users[-1]
            **validated_data
        )

    def update(self, user, validated_data):
        queryset = PersonalModeration.objects.filter(
            user=user, 
            user_to_moderate__id=validated_data.get('user_to_moderate')
        )
        queryset.update(**validated_data)
