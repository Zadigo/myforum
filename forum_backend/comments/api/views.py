from rest_framework import generics
import datetime

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models.functions import ExtractDay

from comments.api import serializers
from comments.api.serializers import CommentSerializer, ValidateComment
from comments.models import Comment, Quote, SavedComment
from comments.permissions import HasCommentPermissions
from threads.api.serializers import MainThreadSerializer
from threads.models import MainThread

USER_MODEL = get_user_model()


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
    queryset = SavedComment.objects.all()
    serializer_class = serializers.SavedCommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        comment = get_object_or_404(Comment, id=pk)

        queryset = self.get_queryset().filter(
            user=request.user,
            comment=comment
        )

        if queryset.exists():
            status_code = status.HTTP_204_NO_CONTENT
            saved_comment = queryset.get()
            saved_comment.delete()
        else:
            saved_comment = SavedComment.objects.create(
                user=request.user,
                comment=comment
            )

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status_code)


@api_view(['get'])
@permission_classes([AllowAny])
def whats_new_view(request, **kwargs):
    queryset = cache.get('whats_new', None)
    if queryset is None:
        threads = MainThread.objects.all()
        cache.set('whats_new', queryset, 3600)
    serializer = MainThreadSerializer(instance=threads, many=True)
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
