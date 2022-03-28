from django.urls import path
from .views import *

app_name = 'main_app'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]