from comments.api.serializers import CommentSerializer
from django.db.models import Case, Value, When
from django.shortcuts import get_object_or_404
from moderation.models import UserModerationPreference
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotAcceptable, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from threads.api import serializers as threads_serializers
from threads.api.serializers import (CustomPageNumberPagination,
                                     ValidateMainThreadSerializer)
from threads.models import MainThread, SubThread
from threads.permissions import HasMainThreadPermissions


class ThreadDetail(generics.RetrieveUpdateAPIView):
    serializer_class = threads_serializers.ThreadSerializer
    queryset = SubThread.objects.filter(active=True)
    permission_classes = [IsAuthenticated]


@api_view(['get'])
def paginated_comments_view(request, pk, **kwargs):
    """Return all the comments for a given thread"""
    thread = get_object_or_404(MainThread, id=pk)
    if not thread.active:
        raise PermissionDenied(detail={'active': 'Thread is not active'})
    comments = thread.comment_set.filter(active=True)

    # If the user is authenticated, get
    # his moderation parameters and other
    # elements that would display the
    # the comments correctly
    if request.user.is_authenticated:
        # TODO: Remove ? Don't know what this does
        # user_profile = request.user.userprofile
        # if user_profile.blocked_users is not None:
        #     blocked_users = user_profile.blocked_users.split(',')
        #     comments = comments.exclude(user__id__in=blocked_users)

        # Remove all the comments that are part of the user's
        # auto-moderation paramaters for comments
        user_moderation = UserModerationPreference.objects.filter(
            user=request.user,
            mute_posts=True
        )
        comments = comments.exclude(
            user__id__in=user_moderation.values_list('id', flat=True)
        )

        # Annotates the comments so that we can know which
        # ones were already bookmarked by the user
        condition = When(savedcomment__user=request.user.id, then=True)
        cases = Case(condition, default=Value(False))
        comments = comments.annotate(bookmarked_by_user=cases)

    # Used to return the number of participants in the thread
    participants = set(comments.values_list('user__username', flat=True))

    paginator = CustomPageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(comments, request=request)

    serializer = CommentSerializer(instance=paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data, participants=len(participants))


class CreateThread(generics.CreateAPIView):
    queryset = SubThread.objects.all()
    serializer_class = ValidateMainThreadSerializer
    permissions = [IsAuthenticated, HasMainThreadPermissions]


@api_view(['post'])
@permission_classes([IsAuthenticated, HasMainThreadPermissions])
def update_view(request, **kwargs):
    pass


@api_view(['delete'])
@permission_classes([IsAuthenticated, HasMainThreadPermissions])
def delete_view(request, pk, **kwargs):
    thread = get_object_or_404(MainThread, pk=pk)

    # Ensure that the user owns the thread
    if thread.user.id != request.user.id:
        raise NotAcceptable(detail='Could not delete thread')

    if not thread.active:
        raise NotAcceptable(detail='Thread is not active')

    thread.delete()
    return Response({'status': True})


@api_view(['post'])
@permission_classes([IsAuthenticated])
def follow_thread(request, pk, **kwargs):
    """Allows the user to follow a given a thread"""
    thread = get_object_or_404(MainThread, pk=pk)
    if not thread.active:
        raise NotAcceptable(detail={'thread': 'Is not active'})

    queryset = thread.followers.filter(id=request.user.id)
    if queryset.exists():
        thread.followers.remove(request.user)
    else:
        thread.followers.add(request.user)
    number_of_followers = thread.followers.count()
    return Response({'state': True, 'number_of_followers': number_of_followers})
