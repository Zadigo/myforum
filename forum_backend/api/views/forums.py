from api.serializers.comments import CommentSerializer
from api.serializers.threads import (ForumSerializer, MainThreadSerializer,
                                     SubThreadSerializer,
                                     ValidateSubThreadSerializer)
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from threads.models import Forum, MainThread, SubThread

from comments.models import USER_MODEL, Comment


class ForumsView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Return active forums or a single active forum"""
    queryset = Forum.objects.filter(active=True)
    serializer_class = ForumSerializer


class ThreadsView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Return all threads or a single
    active thread of the forum"""
    queryset = MainThread.objects.filter(active=True)
    serializer_class = MainThreadSerializer


@api_view(['get'])
def forum_threads_view(request, pk, **kwargs):
    """Return all the threads of a given forum"""
    forum = get_object_or_404(Forum, id=pk)
    threads = forum.mainthread_set.filter(active=True)
    serializer = MainThreadSerializer(instance=threads, many=True)
    return Response(data=serializer.data)

# class ThreadCommentsView(GenericViewSet, ListModelMixin):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

#     def get_queryset(self):
#         queryset = Comment.objects.filter(thread__id=self.kwargs.get('pk'))
#         return queryset


# class SubThreadsView(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin):
#     queryset = SubThread.objects.filter(active=True)
#     serializer_class = ValidateSubThreadSerializer
#     authentication_classes = []
#     permission_classes = []

#     def perform_create(self, serializer):
#         thread = get_object_or_404(MainThread, id=None)
#         user = USER_MODEL.objects.first()
#         serializer.save(user)
        
#         serializer = SubThreadSerializer(instance=self.queryset)
#         return Response(data=serializer.data)
