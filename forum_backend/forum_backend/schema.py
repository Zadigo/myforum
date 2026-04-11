import graphene
from forums.schema import ForumQuery
from polls.schema import PollQuery
from accounts.schema import AccountsQuery
from threads.schema import ThreadQuery
from comments.graphql import queries as comments_queries
from comments.graphql import mutations as comments_mutations

class Query(
    AccountsQuery, 
    ForumQuery, 
    comments_queries.CommentsQuery, 
    PollQuery, 
    ThreadQuery, 
    graphene.ObjectType
):
    pass


class Mutation(graphene.ObjectType):
    create_comments = comments_mutations.CreateComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
