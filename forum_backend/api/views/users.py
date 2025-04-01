from api.serializers.users import UserSerializer
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

USER_MODEL = get_user_model()

@api_view(['get'])
def get_users(request, **kwargs):
    queryset = cache.get('users', None)
    if queryset is None:
        queryset = USER_MODEL.objects.all()
        cache.set('users', queryset, 1200)
        
    searched_value = request.GET.get('user')
    if searched_value is None:
        search = []
    else:
        result = queryset.filter(username__icontains=searched_value)
        search = result.values_list('username', flat=True)
    return Response(data=search)
