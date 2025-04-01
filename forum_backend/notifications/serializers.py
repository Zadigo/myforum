from rest_framework.serializers import Serializer
from rest_framework import fields
from accounts.serializers import UserSerializer

class Notification(Serializer):
    user = UserSerializer()
    message = None
    notification_type = fields.CharField()
    read = fields.BooleanField(default=False)
    created_on = fields.DateField()
