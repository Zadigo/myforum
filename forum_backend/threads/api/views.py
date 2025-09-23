from rest_framework import generics
from polls.models import Answer, Poll
from polls.api import serializers
from celery import group
from comments.api.serializers import CommentSerializer
from django.core.cache import cache
from django.db.models import Case, Q, Value, When
from django.shortcuts import get_object_or_404
from moderation.models import UserModerationPreference
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotAcceptable, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from threads.api import serializers as threads_serializers
from threads.api.serializers import (CustomPageNumberPagination,
                                     ThreadSerializer,
                                     ValidateMainThreadSerializer)
from threads.models import MainThread, SubThread
from threads.permissions import HasMainThreadPermissions


class ThreadDetail(generics.RetrieveUpdateAPIView):
    queryset = MainThread.objects.filter(active=True)
    serializer_class = threads_serializers.ThreadSerializer


class ThreadComments(generics.RetrieveAPIView):
    """Special endpoint that allows us to retrieve comments for
    a specific thread with a statistics wrapper around the comments
    e.g. number of participants, participants etc"""

    queryset = MainThread.objects.filter(active=True)
    serializer_class = threads_serializers.ThreadSerializer

    def apply_query_factors(self, comments):
        """Function used to apply additional factors such
        as the sorting direction etc"""

    def get_object(self):
        thread = super().get_object()

        if not thread.active:
            raise PermissionDenied(detail={'active': 'Thread is not active'})
        return thread

    def get(self, request, pk, *args, **kwargs):
        thread = self.get_object()
        comments = thread.comment_set.filter(active=True)

        # If the user is authenticated, get
        # his moderation parameters and other
        # elements that would display the
        # the comments correctly
        if self.request.user.is_authenticated:
            # Remove all the comments that are part of the
            # user's auto-moderation paramaters for comments

            cache_key1 = f'{self.request.user.id}-ids_to_exclude'
            ids_to_exclude = cache.get(cache_key1, None)
            if ids_to_exclude is None:
                user_moderation = UserModerationPreference.objects.filter(
                    user=self.request.user,
                    mute_all=True
                )
                ids_to_exclude = user_moderation.values_list(
                    'user_to_moderate',
                    flat=True
                )
                cache.set(cache_key1, ids_to_exclude, timeout=(30 * 60))
                comments = comments.exclude(user__id__in=ids_to_exclude)

            # Annotates the comments so that we can know which
            # ones were bookmarked by the user
            condition = When(
                savedcomment__user=self.request.user.id,
                then=True
            )
            cases = Case(condition, default=False)
            comments = comments.annotate(bookmarked_by_user=cases)

        # Used to return the number of participants in the thread
        participants = set(comments.values_list('user__username', flat=True))

        paginator = CustomPageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(
            comments,
            request=self.request
        )

        serializer = CommentSerializer(instance=paginated_queryset, many=True)
        other_data = {
            'participants': participants,
            'participants_count': len(participants),
            'last_activity': comments.last().modified_on
        }
        return paginator.get_paginated_response(serializer.data, **other_data)


class CreateThread(generics.CreateAPIView):
    queryset = MainThread.objects.all()
    serializer_class = ValidateMainThreadSerializer
    permissions = [IsAuthenticated, HasMainThreadPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        serializer = ThreadSerializer(instance=instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()


class DeleteThread(generics.DestroyAPIView):
    queryset = SubThread.objects.filter(active=True)
    serializer_class = threads_serializers.ThreadSerializer

    def perform_destroy(self, instance):
        # Ensure that the user owns the thread
        if instance.user.id != self.request.user.id:
            raise NotAcceptable(detail='Could not delete thread')

        if not instance.active:
            raise NotAcceptable(detail='Thread is not active')

        instance.delete()


class FollowThread(generics.GenericAPIView):
    def post(self, request, pk, *args, **kwargs):
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
        return Response({'number_of_followers': number_of_followers})


class ThreadPoll(generics.RetrieveAPIView):
    """Return the specific poll for the given thread"""

    queryset = Poll.objects.all()
    serializer_class = serializers.PollSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        
        try:
            obj = queryset.get()
        except:
            return None
        else:         
            self.check_object_permissions(self.request, obj)
            return obj

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(thread__id=self.kwargs['pk'])

    def retrieve(self, request, *args, **kwargs):
        template = {'has_poll': False, 'poll': None}
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        if instance is not None:
            template['has_poll'] = True
            template['poll'] = serializer.data

        return Response(template)
