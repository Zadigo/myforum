
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import fields
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from accounts.models import MyUser, PermanentBan, TemporaryBan

USER_MODEL = get_user_model()


class UserProfileSerializer(Serializer):
    preferred_topics = fields.CharField()
    blocked_users = fields.CharField()
    # followers = models.ManyToManyField(
    #     MyUser,
    #     related_name='',
    #     symmetrical=False
    # )
    is_premium = fields.BooleanField()


class UserSerializer(Serializer):
    id = fields.IntegerField(read_only=True)
    username = fields.CharField()
    email = fields.EmailField()
    userprofile = UserProfileSerializer()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def get_response(self):
        if self.instance is None:
            self.is_valid(raise_exception=True)
        return Response(self.data)


# Validators

class Login(Serializer):
    email = fields.EmailField(required=False, allow_null=True)
    username = fields.CharField(required=False, allow_null=True)
    password = fields.CharField()

    def create(self, validated_data):
        username = validated_data.get('username', None)
        email = validated_data.get('email', None)
        if username is None and email is None:
            raise AuthenticationFailed(detail={
                'email': 'Not provided',
                'username': 'Not provided'
            })

        token = None
        logic = (
            Q(username=username) |
            Q(email=email)
        )
        user = get_object_or_404(MyUser, logic)
        result = user.check_password(validated_data['password'])
        if result:
            # 1. Check that the user is active
            if not user.is_active:
                raise AuthenticationFailed(detail='User is not active')

            # 2. Check that the user is active
            if user.permanentban_set.exists():
                raise AuthenticationFailed(detail='User is banned')

            # 3. Check that user is not temporarily
            #    banned from the forum
            try:
                temporary_ban = user.temporaryban_set.latest('created_on')
            except:
                pass
            else:
                if timezone.now() < temporary_ban.end_date:
                    raise AuthenticationFailed(
                        detail=f"User is banned from {temporary_ban.start_date} "
                        f"to {temporary_ban.end_date}"
                    )
                
            token, _ = Token.objects.get_or_create(user=user)
            setattr(self, 'credentials', {'token': str(token)})
        else:
            raise AuthenticationFailed(
                detail="Either username/email or "
                "password are incorrect"
            )
        return user

    # def save(self):
    #     username = self.validated_data.get('username', None)
    #     email = self.validated_data.get('email', None)

    #     if username is None and email is None:
    #         raise AuthenticationFailed(detail='Should provide one of email or username')

    #     token = None
    #     logic = (
    #         Q(username=username) |
    #         Q(email=email)
    #     )
    #     user = get_object_or_404(MyUser, logic)
    #     if user:
    #         result = user.check_password(self.validated_data['password'])
    #         if result:
    #             # 1. Check that that user is active and
    #             # can actually login
    #             if not user.is_active:
    #                 raise AuthenticationFailed(detail='User is not active')

    #             # logic = (
    #             #     Q(user__username=username) |
    #             #     Q(user__email=email)
    #             # )
    #             # # 2. Check that the user is not on the permanent
    #             # # or temporary ban list
    #             # queryset = PermanentBan.objects.filter(logic)
    #             # if queryset.exists():
    #             #     raise AuthenticationFailed(detail='User is permanently banned')

    #             # queryset = TemporaryBan.objects.filter(logic)
    #             # if queryset.exists():
    #             #     latest_ban = queryset.latest()
    #             #     if latest_ban.is_banned:
    #             #         raise AuthenticationFailed(detail=f'User is banned from {latest_ban.start_date} to {latest_ban.end_date}')

    #             token, _ = Token.objects.get_or_create(user=user)
    #         else:
    #             raise AuthenticationFailed(detail='Either username/email or password are incorrect')
    #     return user, {'token': str(token)}

    def get_response(self):
        user = self.save()
        serializer = UserSerializer(instance=user)
        self.credentials.update(serializer.data)
        return Response(self.credentials)
