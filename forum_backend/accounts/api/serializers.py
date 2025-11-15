from accounts.models import UserProfile
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'preferred_topics', 'blocked_users',
            'followers', 'is_premium'
        ]


class UserSerializer(ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'userprofile']


class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']
