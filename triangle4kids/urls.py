"""triangle4kids URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from core import views
from django.urls import path, include
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('index', views.new_index, name='new_index'),
    path('event/<slug>/', views.event_detail, name='event_detail'),
    path('business/', views.business_directory, name='business_directory'),
    path('business/<slug>/', views.business_detail, name='business_detail'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('my-profile/', views.get_user_profile, name="get_user_profile"),
    path(r'(?P<id>\d+)/favorite_event/$',
         views.favorite_event, name='favorite_event'),




]
