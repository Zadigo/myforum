from rest_framework.permissions import BasePermission


class HasMainThreadPermissions(BasePermission):
    permissions = [
        'threads.add_mainthread', 'threads.view_mainthread',
        'threads.delete_mainthread', 'threads.change_mainthread'
    ]

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True

        if request.user.groups.filter(name='Posters').exists():
            return True

        return request.user.has_perms(self.permissions)
