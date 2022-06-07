from django.urls import path
from .views import *

app_name = 'bookmarks'

urlpatterns = [
    path('i/bookmarks/', BookmarksView.as_view(), name='bookmarks'),
]