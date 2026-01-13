import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from threads.models import MainThread, SubThread
from django.db.models import QuerySet


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

    @classmethod
    def get_queryset(cls, queryset: QuerySet[SubThread], info):
        return queryset.select_related('main_thread').order_by('title', '-created_on')


class ThreadQuery(graphene.ObjectType):
    main_thread = graphene.relay.Node.Field(MainThreadNode)
    all_main_threads = DjangoFilterConnectionField(MainThreadNode)

    sub_thread = graphene.relay.Node.Field(SubThreadNode)
    all_sub_threads = DjangoFilterConnectionField(SubThreadNode)
