from rest_framework.permissions import BasePermission

class HasCommentPermissions(BasePermission):
    permissions = [
        'comments.add_comment',
        'comments.change_comment', 
        'comments.delete_comment'
    ]
    
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return request.user.has_perms(self.permissions)
