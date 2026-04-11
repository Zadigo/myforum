import graphene
from graphql import GraphQLResolveInfo
from comments.models import Comment, MediaContent, Quote, Reply
from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField
from base64 import b64decode
from comments.graphql.types import CommentNode, ReplyType, QuoteType, MediaContentType
from comments.utils import OrderingMethods

class CommentsQuery(ObjectType):
    all_comments = DjangoFilterConnectionField(
        CommentNode
    )
    comment = relay.Node.Field(
        CommentNode
    )
    comments_for_thread = DjangoFilterConnectionField(
        CommentNode,
        thread_id=graphene.String(),
        ordering=graphene.String()
    )
    latest_comments = DjangoFilterConnectionField(
        CommentNode, 
        limit=graphene.Int(), 
        default_value=5
    )

    all_replies = graphene.List(
        ReplyType
    )
    reply = graphene.Field(
        ReplyType, 
        reply_id=graphene.Int()
    )
    comment_replies = graphene.List(
        ReplyType, 
        comment_id=graphene.Int()
    )

    all_quotes = graphene.List(
        QuoteType
    )
    comment_quotes = graphene.List(
        QuoteType, comment_id=graphene.Int()
    )

    all_media_contents = graphene.List(
        MediaContentType
    )

    def resolve_all_comments(self, info: GraphQLResolveInfo, **kwargs):
        return Comment.objects.all()

    def resolve_reply(self, info: GraphQLResolveInfo, reply_id):
        return Reply.objects.get(pk=reply_id)

    def resolve_all_replies(self, info: GraphQLResolveInfo):
        related = Reply.objects.prefetch_related('media_contents', 'tags')
        return related.all()

    def resolve_comment_replies(self, info: GraphQLResolveInfo, comment_id):
        related = Reply.objects.prefetch_related('media_contents', 'tags')
        return related.filter(comment__id=comment_id)

    def resolve_all_quotes(self, info: GraphQLResolveInfo):
        return Quote.objects.all()

    def resolve_comment_quotes(self, info: GraphQLResolveInfo, comment_id):
        return Quote.objects.filter(comment__id=comment_id)

    def resolve_all_media_contents(self, info: GraphQLResolveInfo):
        return MediaContent.objects.all()

    def resolve_comments_for_thread(self, info: GraphQLResolveInfo, thread_id: str, ordering: str = None):
        thread_id = int(b64decode(thread_id).decode().split(":")[1])
        qs = Comment.objects.filter(thread__id=thread_id)

        if ordering is not None:
            match ordering:
                case OrderingMethods.MOST_RECENT.value:
                    qs = qs.order_by('-created_on')
                case OrderingMethods.NUMBER_OF_COMMENTS.value:
                    qs = qs.order_by('-replies_count')
                case OrderingMethods.MOST_LIKED.value:
                    qs = qs.order_by('-likes_count')
                case OrderingMethods.LEAST_LIKED.value:
                    qs = qs.order_by('likes_count')
        
        return qs

    def resolve_latest_comments(self, info: GraphQLResolveInfo, limit=5):
        qs = Comment.objects.order_by('-created_on')
        if limit > 10 or limit is None:
            limit = 10
        return qs[:limit]


