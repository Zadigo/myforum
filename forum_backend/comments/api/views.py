from comments.api import serializers
from comments.api.serializers import ValidateComment
from comments.models import Comment, SavedComment
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from threads.api.serializers import ThreadSerializer
from threads.models import MainThread


def edit_comment_helper(request, instance=None):
    """Helper to validate an incoming comment"""
    serializer = ValidateComment(instance=instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    return serializer


class CreateComment(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]


class GetUpdateDeleteComment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]


class BookmarkComment(generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        qs = super().get_queryset()

        comment = get_object_or_404(qs, id=pk)
        status_code = status.HTTP_201_CREATED

        obj, state = SavedComment.objects.get_or_create(
            user=request.user,
            comment=comment
        )

        if state:
            obj.delete()

        serializer = self.get_serializer(instance=comment)
        return Response(data=serializer.data, status=status_code)


@api_view(['get'])
@permission_classes([AllowAny])
def whats_new_view(request, **kwargs):
    queryset = cache.get('whats_new', None)
    if queryset is None:
        threads = MainThread.objects.all()
        cache.set('whats_new', queryset, 3600)
    serializer = ThreadSerializerh(instance=threads, many=True)
    return Response(serializer.data)


class LatestComments(generics.ListAPIView):
    queryset = Comment.objects.filter(created_on__date=timezone.now().date())
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        comments = cache.get('latest_comments', None)
        if comments is None:
            comments = queryset.order_by('-created_on')
            cache.set('latest_comments', comments, (5 * 60))
        return comments[:5]
