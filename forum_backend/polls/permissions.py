from rest_framework.permissions import BasePermission

class HasPollPermissions(BasePermission):
    permissions = ['polls.add_poll', 'polls.view_poll', 
                   'polls.delete_poll', 'polls.change_poll']
    
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        if request.user.groups.filter(name='Posters').exists():
            return True
        
        return request.user.has_perms(self.permissions)
