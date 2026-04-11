from django.db.models import Case
from django.db.models import When
import graphene
from django.db.models import Count
import base64
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLResolveInfo
from threads.models import MainThread, SubThread
from threads.choices import OrderingMethods

class ThreadMixin:
    number_of_comments = graphene.Int()
    is_dead = graphene.Boolean()
    # # raw_participants = graphene.List(graphene.Dynamic)
    # participants = graphene.List(graphene.Int)
    # # latest_comment = graphene.Dynamic(graphene.JSONString())
    # is_new = graphene.Boolean()
    # hot_topic = graphene.Boolean()
    # list_of_participants = graphene.List(
    #     graphene.String,
    #     request=graphene.Argument(graphene.Dynamic)
    # )
    pass


class MainThreadNode(ThreadMixin, DjangoObjectType):
    number_of_comments = graphene.Int(source='num_comments')
    owned_by_user = graphene.Boolean(default_value=False)

    class Meta:
        model = MainThread
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            'user__username': ['exact'],
            'forum__title': ['exact', 'icontains', 'istartswith'],
            'forum__category': ['exact'],
            'forum__description': ['exact', 'icontains', 'istartswith'],
            'title': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'highlighted': ['exact'],
            'published': ['exact'],
            'active': ['exact'],
            'created_on': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'modified_on': ['exact', 'lt', 'gt', 'lte', 'gte']
        }


class SubThreadNode(ThreadMixin, DjangoObjectType):
    class Meta:
        model = SubThread
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            'user__username': ['exact'],
            'forum__title': ['exact', 'icontains', 'istartswith'],
            'forum__category': ['exact'],
            'forum__description': ['exact', 'icontains', 'istartswith'],
            'title': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'highlighted': ['exact'],
            'published': ['exact'],
            'active': ['exact'],
            'created_on': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'modified_on': ['exact', 'lt', 'gt', 'lte', 'gte']
        }


class ThreadQuery(graphene.ObjectType):
    all_main_threads = DjangoFilterConnectionField(
        MainThreadNode
    )
    main_thread = graphene.relay.Node.Field(
        MainThreadNode
    )
    forum_threads = DjangoFilterConnectionField(
        MainThreadNode,
        forum_id=graphene.String(),
        ordering=graphene.String()
    )

    all_sub_threads = DjangoFilterConnectionField(
        SubThreadNode
    )
    sub_thread = graphene.relay.Node.Field(
        SubThreadNode
    )

    def resolve_forum_threads(self, info: GraphQLResolveInfo, forum_id: str=None, **kwargs):
        forum_id = base64.b64decode(forum_id).decode('utf-8').split(':')[-1]
        qs = MainThread.objects.filter(forum__id=forum_id, active=True)
        
        logic = When(user=info.context.user.id, then=True)
        case = Case(logic, default=False)

        qs = qs.annotate(owned_by_user=case, num_comments=Count('comment'))

        ordering = kwargs.get('ordering')
        if ordering is not None:
            match ordering:
                case OrderingMethods.AZ.value:
                    qs = qs.order_by('title')
                case OrderingMethods.ZA.value:
                    qs = qs.order_by('-title')
                case OrderingMethods.MOST_RECENT.value:
                    qs = qs.order_by('-created_on')
                case OrderingMethods.NUMBER_OF_COMMENTS.value:
                    qs = qs.order_by('-num_comments')
        
        return qs
