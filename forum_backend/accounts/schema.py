import graphene
from graphene_django import DjangoObjectType
from accounts.models import UserProfile
from django.contrib.auth import get_user_model


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = '__all__'


class AccountsQuery(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    user_profile = graphene.Field(
        UserProfileType, user_id=graphene.Int(required=True))

    def resolve_user(self, info, id):
        return get_user_model().objects.get(pk=id)

    def resolve_user_profile(self, info, user_id):
        return UserProfile.objects.get(user__id=user_id)
