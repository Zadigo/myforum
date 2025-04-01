from accounts.serializers import UserSerializer
from api.serializers.comments import CommentSerializer
from rest_framework.serializers import Serializer

from notifications.models import Notification


class NotificationSerializer(Serializer):
    user = UserSerializer()
    message = CommentSerializer()

    class Meta:
        model = Notification
        fields = ['user', 'message', 'notification_type', 'read', 'created_on']

    def create(self, validated_data):
        pass
