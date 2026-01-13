from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from forums.models import Forum
from graphene import relay, ObjectType

class ForumNode(DjangoObjectType):
    class Meta:
        model = Forum
        interfaces = (relay.Node,)
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'description': ['icontains'],
            'admin': ['exact'],
            'active': ['exact'],
            'created_on': ['exact', 'lt', 'gt'],
        }


class ForumQuery(ObjectType):
    forum = relay.Node.Field(ForumNode)
    all_forums = DjangoFilterConnectionField(ForumNode)
