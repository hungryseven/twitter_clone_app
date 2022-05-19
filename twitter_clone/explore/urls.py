from django.urls import path
from .views import *

app_name = 'explore'

urlpatterns = [
    path('explore/', ExploreView.as_view(), name='explore'),
    path('search/', SearchView.as_view(), name='search'),
]