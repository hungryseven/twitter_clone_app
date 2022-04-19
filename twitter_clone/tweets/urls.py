from unicodedata import name
from django.urls import path, re_path
from .views import *

app_name = 'tweets'

urlpatterns = [
    re_path(r'^(?P<username>[a-zA-Z0-9_]{4,15})/status/(?P<pk>[0-9]*)/$', DetailtTweetView.as_view(), name='detail_tweet'),
    path('compose/tweet/', MakeTweetView.as_view(), name='make_tweet'),
    path('like/tweet/', LikeTweetView.as_view(), name='like_tweet'),
    path('dislike/tweet/', DislikeTweetView.as_view(), name='dislike_tweet'),
    path('retweet/tweet/', RetweetView.as_view(), name='retweet'),
    path('cancel-retweet/tweet/', CancelRetweetView.as_view(), name='cancel_retweet'),
    path('add-to-bookmarks/tweet/', AddTweetToBookmarksView.as_view(), name='add_to_bookmarks'),
    path('delete-from-bookmarks/tweet/', DeleteTweetFromBookmarksView.as_view(), name='delete_from_bookmarks'),
    path('actions/api/', UserActionsApiView.as_view(), name='actions_api'),
]