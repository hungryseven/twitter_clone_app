"""twitter_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from main_app.views import Error404View, Error505View

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authorization.urls')),
    path('', include('main_app.urls')),
    path('', include('explore.urls')),
    path('', include('tweets.urls')),
    path('', include('user_profile.urls')),
    path('', include('notifications.urls')),
    path('', include('bookmarks.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = Error404View.as_view()
handler505 = Error505View.as_view()