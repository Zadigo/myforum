import datetime

from django.db.models.expressions import Q
from rest_framework import fields
from rest_framework.serializers import Serializer

from comments.models import Comment


class ValidateSearchSerializer(Serializer):
    content = fields.CharField(max_length=100)
    search_titles_only = fields.BooleanField(default=False)
    posted_by = fields.CharField(allow_null=True)
    forums = fields.ListField(allow_null=True)
    include_sub_forums = fields.BooleanField(default=True)
    from_date = fields.DateField(allow_null=True)
    to_date = fields.DateField(allow_null=True)

    def execute_search(self):
        search = self.validated_data['content']
        search_titles_only = self.validated_data['search_titles_only']
        if search_titles_only:
            queryset = Comment.objects.filter(title__icontains=search)
        else:
            queryset = Comment.objects.filter(content__icontains=search)
            
        posted_by = self.validated_data['posted_by']
        if posted_by is not None:
            queryset = queryset.filter(user__username__iexact=posted_by)
            
        from_date = self.validated_data['from_date']
        print(from_date)
        if from_date is not None:
            pass
            # queryset = queryset.filter(created_on__gte=from_date)
        
        to_date = self.validated_data['to_date']
        if to_date is not None:
            pass
            # queryset = queryset.filter(created_on__lte=to_date)
        
        return queryset.order_by('created_on', 'pk')
