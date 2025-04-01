
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import fields
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from accounts.models import MyUser, PermanentBan, TemporaryBan

USER_MODEL = get_user_model()


class UserProfileSerializer(Serializer):
    preferred_topics = fields.CharField()
    blocked_users = fields.CharField()
    # followers = models.ManyToManyField(
    #     MyUser,
    #     related_name='',
    #     symmetrical=False
    # )
    is_premium = fields.BooleanField()


class UserSerializer(Serializer):
    id = fields.IntegerField(read_only=True)
    username = fields.CharField()
    email = fields.EmailField()
    userprofile = UserProfileSerializer()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def get_response(self):
        if self.instance is None:
            self.is_valid(raise_exception=True)
        return Response(self.data)
