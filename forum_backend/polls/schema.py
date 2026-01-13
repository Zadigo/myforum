import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType
from polls.models import Answer, Poll, Possibility


class PossibilityType(DjangoObjectType):
    class Meta:
        model = Possibility
        fields = '__all__'


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = '__all__'


class PollType(DjangoObjectType):
    class Meta:
        model = Poll
        fields = '__all__'


class PollQuery(ObjectType):
    all_polls = graphene.List(PollType)
    poll_by_id = graphene.Field(PollType, id=graphene.Int(required=True))

    def resolve_all_polls(root, info):
        return Poll.objects.all()

    def resolve_poll_by_id(root, info, id):
        try:
            return Poll.objects.get(pk=id)
        except Poll.DoesNotExist:
            return None


class PollMutation(graphene.ObjectType):
    id = graphene.Int()
    question = graphene.String()

    class Arguments:
        thread_id = graphene.Int(required=True)
        question = graphene.String(required=True)
        possibilities = graphene.List(graphene.String, required=True)
        choices_limit = graphene.Int(required=False)
        allow_vote_change = graphene.Boolean(required=False)
        closes = graphene.Boolean(required=False)
        closing_date = graphene.types.datetime.Date(required=False)
        public = graphene.Boolean(required=False)
        voters_alone = graphene.Boolean(required=False)

    def mutate(self, info, thread_id, question, possibilities, **kwargs):
        poll = Poll(
            thread_id=thread_id,
            question=question,
            choices_limit=kwargs.get('choices_limit'),
            allow_vote_change=kwargs.get('allow_vote_change'),
            closes=kwargs.get('closes'),
            closing_date=kwargs.get('closing_date'),
            public=kwargs.get('public'),
            voters_alone=kwargs.get('voters_alone')
        )
        poll.save()


        items = []

        for possibility_text in possibilities:
            items.append(Possibility(poll=poll, text=possibility_text))

        saved_items = Possibility.objects.bulk_create(items)
        poll.possibility_set.set(saved_items)

        return PollMutation(
            id=poll.id,
            question=poll.question
        )
