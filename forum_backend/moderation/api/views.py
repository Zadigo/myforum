from rest_framework.generics import UpdateAPIView, CreateAPIView

from moderation.api.serializers import ValidateReportSerializer


class CreateView(CreateAPIView):
    http_method_names = ['post']
    serializer_class = ValidateReportSerializer
