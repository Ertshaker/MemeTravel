"""
URL configuration for MemeTravel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from Site import views
from Site.views import *

urlpatterns = [
    path('', index),
    path('meme/id<int:pk>', MemeDetailView.as_view()),
    path('user/<slug:username>', UserDetailView.as_view(), name='user-detail'),
    path('admin/', admin.site.urls),
    path('encyclopedia/', encyclopedia),
    path('authorization/', user_register),
    path('login/', user_login),
    path('logout/', user_logout),
    path('user/<str:name>/friends/', friends_view),
    re_path(r'create/(\D*)/$', create_route),
    path('meme/id<int:pk>/update/', MemesUpdateView.as_view()),
    path('remove_friend_request/', views.remove_friend_request, name='remove_friend_request'),
    path('add_friend_request/', views.add_friend_request, name='add_friend_request'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
