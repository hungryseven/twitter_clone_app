from django.urls import path
from .views import *

app_name = 'notifications'

urlpatterns = [
    path('notifications/mentions/', MentionsView.as_view(), name='mentions'),
]