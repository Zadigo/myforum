
from accounts.api.serializers import UserSerializer
from celery import group
from comments import tasks
from comments.models import Comment, Quote, Reply
from django.shortcuts import get_object_or_404
from rest_framework import fields
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from threads.models import MainThread


class QuoteSerializer(Serializer):
    id = fields.IntegerField()


class CommentSerializer(Serializer):
    """Serializer for the Comment model"""

    id = fields.IntegerField()
    thread = fields.CharField(write_only=True)
    user = UserSerializer()
    title = fields.CharField(allow_null=True)
    content = fields.CharField()
    content_delta = fields.JSONField()
    content_html = fields.CharField()
    bookmarked_by_user = fields.BooleanField(default=False)
    # media_contents = MediaContentSerializer(required=False)
    # quote_set = QuoteSerializer(many=True, required=False)
    active = fields.BooleanField(default=True)
    pinned = fields.BooleanField(default=False)
    highlighted = fields.BooleanField(default=False)
    modified_on = fields.DateTimeField()
    created_on = fields.DateTimeField()


class ValidateComment(Serializer):
    thread = fields.IntegerField()
    title = fields.CharField(allow_blank=True, allow_null=True)
    content = fields.CharField()
    content_delta = fields.JSONField()
    content_html = fields.CharField(allow_null=True)
    quotes = fields.ListField()

    def create(self, validated_data):
        request = self._context['request']
        thread = get_object_or_404(
            MainThread,
            id=validated_data['thread']
        )

        new_comment = Comment.objects.create(
            thread=thread,
            user=request.user,
            title=validated_data['title'],
            content=validated_data['content'],
            content_delta=validated_data['content_delta'],
            content_html=validated_data['content_html'],
        )

        t1 = group(
            [
                tasks.analyze_comment.s(new_comment.id, new_comment.content),
                tasks.analyze_comment_with_ai.s(new_comment.id),
                tasks.moderate_comment.s(new_comment.id)
            ]
        )

        t1.apply_async(countdown=30)

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

        t1 = group(
            [
                tasks.analyze_comment_with_ai.s(instance.id),
                tasks.moderate_comment.s(instance.id)
            ]
        )

        t1.apply_async(countdown=5)

        instance.save()
        return instance


class ValidateReply(Serializer):
    comment_id = fields.IntegerField()
    content = fields.CharField()
    content_delta = fields.JSONField()
    content_html = fields.CharField(allow_null=True)
    quotes = fields.ListField()

    def create(self, validated_data):
        user = self._context['request'].user
        
        comment = get_object_or_404(Comment, pk=validated_data['comment_id'])
        
        validated_data.pop('comment_id')
        new_reply = Reply.objects.create(
            user=user,
            comment=comment, 
            **validated_data
        )

        t1 = group(
            [
                tasks.analyze_comment.s(new_reply.id, new_reply.content),
                tasks.analyze_comment_with_ai.s(new_reply.id),
                tasks.moderate_comment.s(new_reply.id)
            ]
        )

        t1.apply_async(countdown=30)

        return new_reply
