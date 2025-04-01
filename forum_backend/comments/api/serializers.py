import pathlib

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from nltk.tokenize import TweetTokenizer
from rest_framework import fields
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from accounts.api.serializers import UserSerializer
from comments.models import Comment, Quote
from moderation.utils import moderate_text
from threads.models import MainThread


class QuoteSerializer(Serializer):
    id = fields.IntegerField()


class CommentSerializer(Serializer):
    """Serializer for the Comment model"""

    id = fields.IntegerField(read_only=True)
    thread = fields.CharField(write_only=True)
    user = UserSerializer(read_only=True)
    title = fields.CharField(read_only=True, allow_null=True)
    content = fields.CharField()
    content_delta = fields.JSONField()
    content_html = fields.CharField()
    bookmarked_by_user = fields.BooleanField(default=False)
    # media_contents = MediaContentSerializer(required=False)
    # quote_set = QuoteSerializer(many=True, required=False)
    active = fields.BooleanField(default=True)
    pinned = fields.BooleanField(read_only=True, default=False)
    bookmarked = fields.BooleanField(read_only=True, default=False)
    highlighted = fields.BooleanField(read_only=True, default=False)
    modified_on = fields.DateTimeField(read_only=True)
    created_on = fields.DateTimeField(read_only=True)

    def analyze(self, comment):
        instance = TweetTokenizer()
        tokens = instance.tokenize(comment)

        moderate_text(tokens=tokens)

        # Map the mentions so that we can send notifications
        # to the people that were mentionned
        mentions = map(lambda x: x.startswith('@'), tokens)
        hashtags = map(lambda x: x.startswith('#'), tokens)

        return comment, list(mentions), list(hashtags)

    def create(self, validated_data):
        request = self._context['request']

        thread = get_object_or_404(
            MainThread,
            id=validated_data['thread']
        )

        # Extract the mentions so that we can eventually
        # notify the users that were mentionned - also,
        # save the hashtags
        content, mentions, hashtags = self.analyze(validated_data['content'])

        # other_params = {'initial_comment': False}
        # count = Comment.objects.count()
        # if count == 0:
        #     other_params['initial_comment'] = True

        new_comment = Comment.objects.create(
            thread=thread,
            user=request.user,
            title=validated_data.get('title', None),
            content=validated_data['content'],
            content_delta=validated_data['content_delta'],
            content_html=validated_data['content_html'],
        )

        quotes = validated_data.get('quotes', [])
        if quotes:
            quote_objs = []
            for quote_id in quotes:
                comment_to_quote = get_object_or_404(Comment, pk=quote_id)
                quote_objs.append(Quote(
                    comment=new_comment,
                    quoted_comment=comment_to_quote,
                    content=comment_to_quote.content,
                    content_html=comment_to_quote.content_html
                ))
            quotes = Quote.objects.bulk_create(quote_objs)

        return new_comment

    def update(self, instance, validated_data):
        exclude_fields = ['thread']
        for field in validated_data.keys():
            if field in exclude_fields:
                continue
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance


class SavedCommentSerializer(Serializer):
    id = fields.IntegerField()
    comment = CommentSerializer()


# Validators

class ValidateComment(Serializer):
    title = fields.CharField(allow_null=True)
    content = fields.CharField()
    content_delta = fields.JSONField()
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

    def save(self, request, **kwargs):
        setattr(self, 'request', request)
        return super().save(**kwargs)

    def create(self, validated_data):
        thread = get_object_or_404(
            MainThread,
            id=validated_data['thread']
        )

        # Extract the mentions so that we can eventually
        # notify the users that were mentionned - also,
        # save the hashtags
        content, mentions, hashtags = self.analyze(validated_data['content'])
        new_comment = Comment.objects.create(
            thread=thread,
            user=self.request.user,
            title=validated_data['title'],
            content=validated_data['content'],
            content_delta=validated_data['content_delta'],
            content_html=validated_data['content_html'],
        )

        quotes = validated_data['quotes']
        if quotes:
            quote_objs = []
            for quote_id in quotes:
                comment_to_quote = get_object_or_404(Comment, pk=quote_id)
                quote_objs.append(Quote(
                    comment=new_comment,
                    quoted_comment=comment_to_quote,
                    content=comment_to_quote.content,
                    content_html=comment_to_quote.content_html
                ))
            quotes = Quote.objects.bulk_create(quote_objs)

        return new_comment

    def update(self, instance, validated_data):
        exclude_fields = ['thread']
        for field in validated_data.keys():
            if field in exclude_fields:
                continue
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance

    def get_response(self, request):
        instance = self.save(request)
        serializer = CommentSerializer(instance=instance)
        return Response(serializer.data)
