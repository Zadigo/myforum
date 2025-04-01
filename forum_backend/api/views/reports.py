from api.serializers.reports import ReportSerializer
from django.contrib.auth import get_user_model
from moderation.models import Report
from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

USER_MODEL = get_user_model()

class ReportView(GenericViewSet, CreateModelMixin):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = []
    permission_classes = []

    def perform_create(self, serializer):
        # TEST:
        user = USER_MODEL.objects.first()
        serializer.save(user=user)
