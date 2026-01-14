from django.shortcuts import get_object_or_404
import graphene
from forums.models import Forum
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


class ForumNode(DjangoObjectType):
    number_of_threads = graphene.Int()

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
    
