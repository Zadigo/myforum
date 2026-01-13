import graphene
from forums.schema import ForumQuery
from comments.schema import CommentsQuery, CommentsMutation
from polls.schema import PollQuery
from accounts.schema import AccountsQuery
from threads.schema import ThreadQuery


class Query(AccountsQuery, ForumQuery, CommentsQuery, PollQuery, ThreadQuery, graphene.ObjectType):
    pass


class Mutation(CommentsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
