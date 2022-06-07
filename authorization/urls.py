from django.urls import path
from .views import *

app_name = 'authorization'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]