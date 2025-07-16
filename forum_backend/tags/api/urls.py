from django.urls import re_path
from tags.api import views

app_name = 'api_tags'

urlpatterns = [
    re_path(
        r'search$', 
        views.SearchTags.as_view(), 
        name='search'
    )
]
