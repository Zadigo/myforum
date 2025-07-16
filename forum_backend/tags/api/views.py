from django.core.cache import cache
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from tags.api.serializers import TagSerializer
from tags.models import Tag


class SearchTags(generics.GenericAPIView):
    """API view to search for tags"""

    serializer_class = TagSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')

        if query is None:
            return Response([], status=status.HTTP_200_OK)

        tags = cache.get(f'tags_search_{query}', [])
        if not tags:
            tags = Tag.objects.filter(name__icontains=query)
            cache.set(f'tags_search_{query}', tags, 60 * 60)

        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
