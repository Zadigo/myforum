from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from comments.models import Comment
from forums.models import Forum
from threads.api.serializers import ForumSerializer, MainThreadSerializer

# class ForumsView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
#     """Return active forums or a single active forum"""
#     queryset = Forum.objects.filter(active=True)
#     serializer_class = ForumSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)

#         data = serializer.data
#         # Return some basic statistics for the forum
#         total_number_of_comments = cache.get('total_number_of_comments', None)
#         if total_number_of_comments is None:
#             total_number_of_comments = Comment.objects.count()
#             cache.set('total_number_of_comments',
#                       total_number_of_comments, 12000)
#         # data['total_number_of_comments'] = total_number_of_comments

#         # Latest comments
#         # comments = cache.get('comments', None)
#         # if comments is None:
#         #     cache.set('commens', Comment.objects.all(), 3600)
#         return Response(data)
