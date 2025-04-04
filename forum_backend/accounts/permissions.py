from rest_framework.permissions import BasePermission
from accounts.models import PermanentBan, TemporaryBan
from django.core.cache import cache


class IsBanned(BasePermission):
    def is_banned(self, cache_key, model, request):
        users = cache.get(cache_key, None)
        if users is None:
            users = model.objects.filter(user=request.user)
            cache.set(cache_key, users, timeout=15*60)
        return users.exists()

    def has_permission(self, request, **kwargs):
        result = [
            self.is_banned(PermanentBan, request),
            self.is_banned(TemporaryBan, request)
        ]
        return all(result)
