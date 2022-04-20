from django.urls import re_path, path
from .views import *

app_name = 'user_profile'

urlpatterns = [
    re_path(r'^(?P<username>[a-zA-Z0-9_]{4,15})/$', ProfileTweetsView.as_view(), name='profile_tweets'),
    re_path(r'^(?P<username>[a-zA-Z0-9_]{4,15})/with_replies/$', ProfileRepliesView.as_view(), name='profile_replies'),
    re_path(r'^(?P<username>[a-zA-Z0-9_]{4,15})/likes/$', ProfileLikesView.as_view(), name='profile_likes'),
]