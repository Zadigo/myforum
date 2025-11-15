from notifications import models
from notifications.api import serializers
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class NotificationApi(ListAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
