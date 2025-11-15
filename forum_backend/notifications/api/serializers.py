from rest_framework import serializers
from notifications import models
from accounts.api.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Notification
        fields = ['id', 'user', 'message', 'read', 'created_on']
