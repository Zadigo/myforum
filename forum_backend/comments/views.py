import datetime

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from threads.models import MainThread
from threads.serializers import MainThreadSerializer

from comments.models import Comment, Quote, SavedComment
from comments.permissions import HasCommentPermissions
from comments.serializers import CommentSerializer, ValidateComment

USER_MODEL = get_user_model()

def edit_comment_helper(request, instance=None):
    serializer = ValidateComment(instance=instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    return serializer


@api_view(['post'])
@permission_classes([IsAuthenticated, HasCommentPermissions])
def create_view(request, **kwargs):
    serializer = edit_comment_helper(request)
    serializer.save(request)
    return serializer.get_response(request)


@api_view(['post'])
@permission_classes([IsAuthenticated, HasCommentPermissions])
def update_view(request, pk, **kwargs):
    comment = get_object_or_404(Comment, id=pk)
    serializer = edit_comment_helper(request, instance=comment)
    serializer.update()
    return serializer.get_response()


@api_view(['post'])
@permission_classes([IsAuthenticated])
def bookmark_comment_view(request, pk, **kwargs):
    comment = get_object_or_404(Comment, id=pk)
    if request.user.is_authenticated:
        saved_comment = SavedComment.objects.filter(
            user=request.user,
            comment=comment
        )
        if saved_comment.exists():
            saved_comment.delete()
        else:
            saved_comment = SavedComment.objects.create(
                user=request.user,
                comment=comment
            )
        return Response(data={'status': True})
    raise ValidationError(detail='No auhenticated', code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['get'])
@permission_classes([AllowAny])
def whats_new_view(request, **kwargs):
    queryset = cache.get('whats_new', None)
    if queryset is None:
        threads = MainThread.objects.all()
        cache.set('whats_new', queryset, 3600)
    serializer = MainThreadSerializer(instance=threads, many=True)
    return Response(serializer.data)


@api_view(['get'])
@permission_classes([AllowAny])
def latest_comments_view(request, **kwargs):
    latest_comments = cache.get('latest_comments', None)
    
    if latest_comments is None:
        latest_comment = Comment.objects.latest('created_on')        
        result = latest_comment - datetime.timedelta(hours=1)
        comments = Comment.objects.filter(gte=result, lte=latest_comment.created_on)
        cache.set('latest_comments', comments, 1000)
        
    serializer = CommentSerializer(instance=comments, many=True)
    return serializer.get_response()
