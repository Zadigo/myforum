
from django.contrib.auth import get_user_model
from rest_framework import fields
from rest_framework.serializers import Serializer

USER_MODEL = get_user_model()

class UserSerializer(Serializer):
    id = fields.IntegerField(read_only=True)
    username = fields.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
