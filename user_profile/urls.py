from django.urls import re_path, path
from .views import *

app_name = 'user_profile'

urlpatterns = [
    re_path(r'^(?P<username>[a-zA-Z0-9_]{4,15})/$', ProfileTweetsView.as_view(), name='profile_tweets'),
    re_path(r'^(?P<username>[a-zA-Z0-9_]{4,15})/with_replies/$', ProfileRepliesView.as_view(), name='profile_replies'),
    re_path(r'^(?P<username>[a-zA-Z0-9_]{4,15})/likes/$', ProfileLikesView.as_view(), name='profile_likes'),
    re_path(r'^(?P<username>[a-zA-Z0-9_]{4,15})/followers/$', FollowersView.as_view(), name='user_followers'),
    re_path(r'^(?P<username>[a-zA-Z0-9_]{4,15})/following/$', FollowingView.as_view(), name='user_following'),
    re_path(r'^(?P<username>[a-zA-Z0-9_]{4,15})/followers_you_follow/$', FollowersYouFollowView.as_view(), name='followers_you_follow'),
    path('friendship/create/', FollowUserView.as_view(), name='follow_user'),
    path('friendship/destroy/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('follow/api/', UserFollowApiView.as_view(), name='follow_api'),
]