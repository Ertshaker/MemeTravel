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
from django.contrib import admin
from django.urls import path, re_path
from Site.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index),
    path('meme/id<int:pk>', MemeDetailView.as_view()),
    path('user/<slug:username>', UserDetailView.as_view()),
    path('admin/', admin.site.urls),
    path('encyclopedia/', encyclopedia),
    path('authorization/', user_register),
    path('login/', user_login),
    path('logout/', user_logout),
    path('profile/', profile_view),
    path('test/', test_view),
    path('another_test_subject', auth_views.PasswordChangeView.as_view()),
    path('user/<str:name>/friends/', friends_view),
    re_path(r'create/(\D*)/$', create_route)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)