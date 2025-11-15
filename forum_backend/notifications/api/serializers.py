from rest_framework import serializers
from notifications import models
from accounts.api.serializers import SimpleUserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = models.Notification
        fields = ['id', 'user', 'message', 'read', 'created_on']
