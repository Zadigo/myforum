from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers.search import ValidateSearchSerializer
from comments.api.serializers import CommentSerializer


@api_view(['post'])
def search(request, **kwargs):
    serializer = ValidateSearchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    queryset = serializer.execute_search()
    comment_serializer = CommentSerializer(instance=queryset, many=True)
    return Response(data=comment_serializer.data)
