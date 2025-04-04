from polls.api import serializers
from polls.models import Answer, Poll
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class GetPoll(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = serializers.PollSerializer


class AnswerPoll(generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = serializers.ValidateAnswer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['poll'] = self.get_object()
        return context


class GetPollAnswers(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(poll__id=self.kwargs['pk'])
