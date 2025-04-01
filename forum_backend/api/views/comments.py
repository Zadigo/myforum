

from api.permission import HasCommentPermissions
from api.serializers.comments import (CommentSerializer,
                                      CustomPageNumberPagination,
                                      QuoteSerializer,
                                      ValidateCommentSerializer)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from threads.models import MainThread

from comments.models import Comment, Quote, SavedComment

USER_MODEL = get_user_model()


class CommentsView(GenericViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    """Allows creation, updating and destruction of a comment"""
    queryset = Comment.objects.filter(active=True)
    serializer_class = ValidateCommentSerializer
    permission_classes = [IsAuthenticated, HasCommentPermissions]        
        
    def perform_create(self, request, serializer):
        serializer.save(request)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(request, serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, headers=headers, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(
            comment,
            data=request.data,
            partial=kwargs.get('partial')
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.update()
        serializer = CommentSerializer(instance=comment)
        return Response(data=serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         comment = self.get_object()
#         comment.delete()

#         comments_serializer = CommentSerializer(instance=self.queryset, many=True)
#         return Response(data=comments_serializer.data)


# class QuotesView(GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin):
#     queryset = Quote.objects.all()
#     serializer_class = QuoteSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = Quote.objects.filter(message__id=1)

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         comment = get_object_or_404(Comment, id=kwargs.get('id'))
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         quote = serializer.create(comment)
#         serializer = self.get_serializer(instance=quote)
#         return Response(data=serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)


@api_view(['get'])
def comments_view(request, pk, **kwargs):
    """Return all the comments from a given thread"""
    thread = get_object_or_404(MainThread, id=pk)
    comments = thread.comment_set.filter(active=True)

    paginator = CustomPageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(comments, request=request)

    serializer = CommentSerializer(instance=paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)
