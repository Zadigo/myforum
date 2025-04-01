from rest_framework import fields
from rest_framework.serializers import ModelSerializer, Serializer

from accounts.api.serializers import UserSerializer
from moderation.models import Report


class UserModerationPreferenceSerializer(Serializer):
    """Serializer for UserModerationPreference model"""

    id = fields.IntegerField()
    user_to_moderate = UserSerializer()
    mute_all = fields.BooleanField()
    mute_posts = fields.BooleanField()
    mute_threads = fields.BooleanField()
    direct_messages = fields.BooleanField()


class ValidateReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = ['comment', 'thread', 'user']
