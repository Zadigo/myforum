from accounts.api.serializers import UserSerializer
from accounts.models import PermanentBan, TemporaryBan
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class Profile(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        user = get_object_or_404(queryset, id=self.request.user.id)
        self.check_object_permissions(self.request, user)

        params = {'user': self.request.user}
        permaban_qs = PermanentBan.objects.filter(**params)
        temporary_ban_qs = TemporaryBan.objects.filter(**params)

        is_banned = [
            permaban_qs.exists(),
            temporary_ban_qs.exists()
        ]

        if any(is_banned):
            raise PermissionDenied('No authorized')

        return user
