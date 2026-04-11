from typing import Any

import graphene
from graphql import GraphQLResolveInfo
from comments.models import Comment, Tag


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

    def mutate(self, info: GraphQLResolveInfo, **kwargs: Any):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Authentication required")
        
        thread_id = kwargs.get('thread_id')
        title = kwargs.get('title', '')
        pinned = kwargs.get('pinned', False)
        original_post = kwargs.get('original_post', False)
        content = kwargs.get('content', '')
        content_delta = kwargs.get('content_delta')
        content_html = kwargs.get('content_html')
        tags = kwargs.get('tags', [])

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

        # TODO: Morderate the comment content here 
        # (e.g., check for profanity, spam, etc.)

        if tags:
            tags_to_add = []
            for name in tags:
                tag, created = Tag.objects.get_or_create(name=name)
                tags_to_add.append(tag)
            comment.tags.add(*tags_to_add)

        comment.save()

        # TODO: Moderate tags here 
        # (e.g., check for inappropriate tags, etc.)

        return CreateComment(
            title=comment.title,
            content_html=comment.content_html
        )
