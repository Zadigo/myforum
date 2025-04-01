from rest_framework import fields
from rest_framework.serializers import Serializer

from accounts.serializers import UserSerializer


class ForumSerializer(Serializer):
    """Serializer for the Forum model"""

    id = fields.IntegerField()
    user = UserSerializer()
    title = fields.CharField()
    category = fields.CharField()
    description = fields.CharField()
    admin = fields.BooleanField(default=False)
    number_of_threads = fields.IntegerField()
    active = fields.BooleanField(default=True)
    created_on = fields.DateTimeField()
