from django.db.models import Case
from django.db.models import When
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from threads.models import MainThread, SubThread


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

    # @classmethod
    # def get_queryset(cls, queryset: QuerySet[SubThread], info):
    #     return queryset.select_related('main_thread').order_by('title', '-created_on')


class ThreadQuery(graphene.ObjectType):
    main_thread = graphene.relay.Node.Field(MainThreadNode)
    all_main_threads = DjangoFilterConnectionField(MainThreadNode)

    forum_threads = DjangoFilterConnectionField(
        MainThreadNode,
        forum_id=graphene.Int()
    )

    sub_thread = graphene.relay.Node.Field(SubThreadNode)
    all_sub_threads = DjangoFilterConnectionField(SubThreadNode)

    def resolve_forum_threads(self, info, forum_id=None, **kwargs):
        qs = MainThread.objects.filter(forum__id=forum_id, active=True)
        logic = When(user=info.context.user, then=True)
        case = Case(logic, default=False)
        return qs.annotate(owned_by_user=case)
