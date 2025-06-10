from django.db.models import Case, Count, Value, When
from django.shortcuts import get_object_or_404
from forums.api import serializers
from forums.models import Forum
from rest_framework import generics
from rest_framework.response import Response
from threads.api import serializers as threads_serializers
from threads.models import MainThread
from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    page_size = 30


class ForumDetails(generics.RetrieveAPIView):
    serializer_class = serializers.ForumSerializer
    queryset = Forum.objects.filter(active=True)


class ListForums(generics.ListAPIView):
    serializer_class = serializers.ForumSerializer
    queryset = Forum.objects.filter(active=True)


class ForumThreads(generics.GenericAPIView):
    serializer_class = threads_serializers.ThreadSerializer
    queryset = MainThread.objects.filter(active=True)
    pagination_class = BasePagination

    def get(self, request, pk, *args, **kwargs):
        forum = get_object_or_404(Forum, id=pk)
        threads = forum.mainthread_set.all()

        sorting_methods = [
            'Sort alphabetically A-Z',
            'Sort alphabetically Z-A',
            'Most recent',
            'Number of comments'
        ]

        sorting_method = int(request.GET.get('sort', 0))
        if sorting_method > len(sorting_methods):
            sorting_method = 0

        if sorting_method == 0:
            threads = threads.order_by('title')

        if sorting_method == 1:
            threads = threads.order_by('-title')

        if sorting_method == 2:
            threads = threads.order_by('-created_on')

        if sorting_method == 3:
            annotated_threads = threads.annotate(
                number_of_comments=Count('comment')
            )
            threads = annotated_threads.order_by('-number_of_comments')

        if request.user.is_authenticated:
            condition = When(user=request.user, then=True)
            case = Case(condition, default=Value(False))
            threads = threads.annotate(owned_by_user=case)

        serializer = self.get_serializer(instance=threads, many=True)

        data = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(data)


class FollowForum(generics.CreateAPIView):
    pass
