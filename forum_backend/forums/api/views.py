from django.db.models import Case, Count, Value, When
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from forums.models import Forum
from threads.api import serializers


@api_view(['get'])
def forums_view(request, **kwargs):
    """List all the forums from the database"""
    queryset = Forum.objects.all()
    serializer = serializers.ForumSerializer(
        instance=queryset,
        many=True
    )
    return Response(serializer.data)


@api_view(['get'])
def forum_threads_view(request, pk, **kwargs):
    """List of the threads located in a forum
    from the database"""
    forum = get_object_or_404(Forum, id=pk)
    threads = forum.mainthread_set.all()

    sorting_methods = [
        'Sort alphabetically A-Z', 'Sort alphabetically Z-A',
        'Most recent', 'Number of comments'
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

    serializer = serializers.MainThreadSerializer(
        instance=threads,
        many=True
    )
    return Response(serializer.data)


@api_view(['post'])
def follow_forum_view(request, pk, **kwargs):
    pass
