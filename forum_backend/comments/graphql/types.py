import graphene
from comments.models import Comment, MediaContent, Quote, Reply
from graphene import relay
from graphene_django import DjangoObjectType


class MediaContentType(DjangoObjectType):
    class Meta:
        model = MediaContent
        fields = (
            'id',
            'media_content_id',
            'image',
            'image_thumbnail',
            'file',
            'video',
            'created_on'
        )


class QuoteType(DjangoObjectType):
    class Meta:
        model = Quote
        fields = (
            'id',
            'comment',
            'quoted_comment',
            'content',
            'content_html',
            'modified_on',
            'created_on',
        )


class ReplyType(DjangoObjectType):
    class Meta:
        model = Reply
        fields = (
            'id',
            'user',
            'content',
            'content_delta',
            'content_html',
            'media_contents',
            'tags',
            'active',
            'modified_on',
            'created_on',
        )


class CommentNode(DjangoObjectType):
    bookmarked_by_user = graphene.Boolean(default_value=False)

    class Meta:
        model = Comment
        interfaces = (relay.Node,)
        filter_fields = {
            'thread__id': ['exact'],
            'thread__title': ['icontains', 'istartswith'],
            'subthread__title': ['icontains'],
            'title': ['icontains', 'istartswith'],
            'pinned': ['exact'],
            'original_post': ['exact'],
            'publish_on': ['exact', 'lt', 'gt'],
            'published': ['exact']
        }
