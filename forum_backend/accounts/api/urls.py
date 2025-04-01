from django.urls import re_path
from accounts.api import views

app_name = 'accounts_api'

urlpatterns = [
    re_path(
        r'^profile$', 
        views.Profile.as_view(), 
        name='profile'
    )
]
