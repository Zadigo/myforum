import graphene
from comments.models import Comment, MediaContent, Quote, Reply, Tag
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


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


class CommentsQuery(ObjectType):
    comment = relay.Node.Field(CommentNode)
    all_comments = DjangoFilterConnectionField(CommentNode)

    reply = graphene.Field(ReplyType, reply_id=graphene.Int())
    all_replies = graphene.List(ReplyType)
    comment_replies = graphene.List(ReplyType, comment_id=graphene.Int())

    all_quotes = graphene.List(QuoteType)
    comment_quotes = graphene.List(QuoteType, comment_id=graphene.Int())

    all_media_contents = graphene.List(MediaContentType)

    def resolve_reply(self, info, reply_id):
        return Reply.objects.get(pk=reply_id)

    def resolve_all_replies(self, info):
        related = Reply.objects.prefetch_related('media_contents', 'tags')
        return related.all()

    def resolve_comment_replies(self, info, comment_id):
        related = Reply.objects.prefetch_related('media_contents', 'tags')
        return related.filter(comment__id=comment_id)

    def resolve_all_quotes(self, info):
        return Quote.objects.all()

    def resolve_comment_quotes(self, info, comment_id):
        return Quote.objects.filter(comment__id=comment_id)

    def resolve_all_media_contents(self, info):
        return MediaContent.objects.all()


class CreateComment(graphene.Mutation):
    title = graphene.String()
    content_html = graphene.String()

    class Arguments:
        thread_id = graphene.Int(required=True)
        title = graphene.String(required=False)
        pinned = graphene.Boolean(required=False, default_value=False)
        original_post = graphene.Boolean(required=False, default_value=False)
        content = graphene.String(required=False)
        content_delta = graphene.String(required=True)
        content_html = graphene.String(required=True)
        tags = graphene.List(graphene.String, required=False)

    def mutate(self, info, thread_id, content_delta, content_html, title=None, pinned=False, original_post=False, content=None, tags=None):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Authentication required")

        comment = Comment(
            user=user,
            thread_id=thread_id,
            title=title,
            pinned=pinned,
            original_post=original_post,
            content=content,
            content_delta=content_delta,
            content_html=content_html
        )
        comment.save()

        if tags:
            for tag_name in tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                comment.tags.add(tag_obj)

        comment.save()

        return CreateComment(
            title=comment.title,
            content_html=comment.content_html
        )


class CommentsMutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
