from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from polls.models import Poll
from polls.permissions import HasPollPermissions
from polls.serializers import (PollSerializer, ValidateAnswer,
                               ValidatePollSerializer)


@api_view(['post'])
@permission_classes([IsAuthenticated, HasPollPermissions])
def create_view(request, **kwargs):
    serializer = ValidatePollSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(request)
    return serializer.get_response()


@api_view(['get'])
def poll_view(request, pk, **kwargs):
    """Returns the poll for the current thread"""
    queryset = Poll.objects.filter(thread__id=pk)
    try:
        poll = queryset.get()
    except:
        return Response({'has_poll': False})
        
    serializer = PollSerializer(instance=poll)
    
    data = serializer.data
    data['has_answered'] = False
    
    if request.user.is_authenticated:
        has_answered = poll.answer_set.filter(
            poll=poll,
            user=request.user
        )
        data['has_answered'] = has_answered.exists()
    data['has_poll'] = True
    return Response(data)


@api_view(['post'])
def answer_poll_view(request, pk, **kwargs):
    serializer = ValidateAnswer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(request, pk)
    return Response({'status': True})
