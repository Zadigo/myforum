import pathlib

from accounts.serializers import UserSerializer
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from nltk.tokenize import TweetTokenizer
from rest_framework import fields
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from moderation.utils import moderate_text
from threads.models import MainThread
from rest_framework.response import Response

from comments.models import Comment


class QuoteSerializer(Serializer):
    id = fields.IntegerField()


class CommentSerializer(Serializer):
    id = fields.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)

    title = fields.CharField(allow_null=True)
    content = fields.CharField()

    # media_contents = MediaContentSerializer(required=False)
    # quote_set = QuoteSerializer(many=True, required=False)

    active = fields.BooleanField(default=True)
    pinned = fields.BooleanField(default=False)
    bookmarked = fields.BooleanField(default=False)
    highlighted = fields.BooleanField(default=False)

    modified_on = fields.DateTimeField(required=False)
    created_on = fields.DateTimeField(required=False)


class ValidateComment(Serializer):
    title = fields.CharField(allow_null=True)
    content = fields.CharField()
    content_html = fields.CharField(allow_null=True)
    thread = fields.IntegerField()
    quotes = fields.ListField()
            
    def analyze(self, comment):
        instance = TweetTokenizer()
        tokens = instance.tokenize(comment)
        
        moderate_text(tokens=tokens)
        
        # Map the mentions so that we can send notifications
        # to the people that were mentionned
        mentions = map(lambda x: x.startswith('@'), tokens)
        hashtags = map(lambda x: x.startswith('#'), tokens)
        
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
            for key, value in self.validated_data.items():
                if key not in exclude_fields:
                    setattr(self.instance, key, value)
            self.instance.save()
        return self.instance

    def get_response(self, request):
        instance = self.save(request)
        serializer = CommentSerializer(instance=instance)
        return Response(serializer.data)
