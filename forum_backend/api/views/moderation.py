from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from moderation.models import PersonalModeration
from api.serializers.moderation import PersonalModerationSerializer


class ModerationView(GenericViewSet, CreateModelMixin, UpdateModelMixin):
    queryset = PersonalModeration
    serializer_class = PersonalModerationSerializer
    authentication_classes = []
    permission_classes = []
