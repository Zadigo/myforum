import pathlib

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from nltk.tokenize import TweetTokenizer
from rest_framework import fields
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer

from accounts.serializers import UserSerializer
from api import validators
from api.serializers.mixins import SerializerMixin
from api.serializers.threads import MainThreadSerializer, SubThreadSerializer
from comments.models import Comment, MediaContent, Quote
from threads.models import MainThread


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 30
    
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['pages'] = self.page.paginator.num_pages
        return response


class QuoteSerializer(Serializer):
    id = fields.IntegerField()


class MediaContentSerializer(ModelSerializer):
    class Meta:
        model = MediaContent
        fields = ['image', 'image_thumbnail', 'file', 'video', 'created_on']


class CommentSerializer(Serializer):
    id = fields.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)

    title = fields.CharField(allow_null=True)
    content = fields.CharField()

    # media_contents = MediaContentSerializer(required=False)
    # quote_set = QuoteSerializer(many=True, required=False)

    active = fields.BooleanField(default=True)
    pinned = fields.BooleanField(default=False)
    highlighted = fields.BooleanField(default=False)
    
    modified_on = fields.DateTimeField(required=False)
    created_on = fields.DateTimeField(required=False)
    
    def get_response(self):
        return Response(self.data)


class QuoteSerializer(Serializer):
    id = fields.IntegerField(read_only=True)

    # def create(self, comment):
    #     return comment.quote_set.create()


class ValidateComment(Serializer):
    thread = fields.IntegerField()
    title = fields.CharField(allow_null=True)
    content = fields.CharField()
    content_html = fields.CharField(allow_null=True)
    quotes = QuoteSerializer(required=False)
    
    @staticmethod
    def moderate(tokens):
        """Does a quick validation of the comment. This
        is not a full formal validation done by a moderator"""
        stop_words = cache.get('stop_words', None)
        if stop_words is None:
            file_path = pathlib.Path(settings.MEDIA_URL, 'stop_words')
            with open(file_path, mode='r', encoding='utf-8') as f:
                stop_words = f.readlines()
                cache.set('stop_words', stop_words, 3600)
                
        invalid_words = list(map(lambda x: x, tokens))
        
        if invalid_words:
            raise ValidationError(detail='Comment contains invdalid words ')
        
    def queryset(self):
        return Comment.objects.filter(thread__id=self.validated_data['thread'])
        
    def analyze(self, comment):
        instance = TweetTokenizer()
        tokens = instance.tokenize(comment)
        
        self.moderate(tokens)
        
        mentions = map(lambda x: x.startswith('@'))
        hashtags = map(lambda x: x.startswith('#'))
        
        return comment, list(mentions), list(hashtags)
        
    def save(self, request):
        thread = get_object_or_404(MainThread, id=self.validated_data['thread'])
        content, mentions, hashtags = self.analyze(self.validated_data['content'])
        instance = Comment.objects.create(
            thread=thread,
            user=request.user,
            title=self.validated_data['title'],
            content=content,
            content_html=self.validated_data['content_html']
        )
        return instance

    def update(self):
        if self.instance:
            exclude_fields = ['thread']
            content, mentions, hashtags = self.analyze(self.validated_data['content'])
            for key, value in self.validated_data.items():
                if key not in exclude_fields:
                    setattr(self.instance, key, value)
            self.instance.save()
        return self.instance
    
    def get_response(self):
        serializer = CommentSerializer(instance=self.queryset(), many=True)
        return Response(serializer.data)
