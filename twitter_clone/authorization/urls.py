from django.urls import path
from .views import *

app_name = 'authorization'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]