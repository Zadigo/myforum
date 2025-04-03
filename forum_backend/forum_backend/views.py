from comments.api.serializers import CommentSerializer
from comments.models import Comment
from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response


class Search(generics.GenericAPIView):
    def post(self, request, *args, **kwags):
        search = request.data.get('q', None)
        search_titles_only = request.data.get('search_titles_only', False)
        posted_by = request.data.get('posted_by', None)
        date_from = request.data.get('from', None)
        date_to = request.data.get('to', None)

        template = {
            'threads': [],
            'comments': []
        }

        if search is not None:
            logic = (
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(user__username__icontains=search)
            )

            if posted_by is not None:
                logic = logic & Q(user__username=posted_by)

            comments = Comment.objects.filter(
                logic).order_by('-created_on', 'pk')
            s1 = CommentSerializer(instance=comments, many=True)

            # sub_threads = SubThread.objects.filter(
            #     logic).order_by('-created_on', 'pk')
            # s2 = SubThreadSerializer(instance=sub_threads, many=True)

            if date_from is not None:
                pass

            if date_to is not None:
                pass

            template['comments'] = s1.data
            # template['threads'] = s2.data
        return Response(data=template)


@api_view(['post'])
def search_view(request, **kwargs):
    """Allows a user to search the forum"""
    search = request.data.get('q', None)
    return_data = {
        'threads': [],
        'comments': []
    }
    if search is not None:
        logic = (
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(user__username__icontains=search)
        )
        comments = Comment.objects.filter(logic).order_by('-created_on', 'pk')
        comments_serializer = CommentSerializer(instance=comments, many=True)
        return_data.update(comments=comments_serializer.data)
    return Response(return_data)
