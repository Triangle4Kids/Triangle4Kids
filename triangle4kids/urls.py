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
# from core.views import EventListView
# from core.views import search
from . import settings
from core import views
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from django.views.generic import TemplateView

from core.views import BusinessResultsListView, EventResultsListView

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls import url, include
from django.contrib.auth.models import User

from rest_framework import routers
from api import views as api_views

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('businesses', api_views.BusinessViewset,
                api_views.BusinessLatLongViewset)
router.register('businesseslocation', api_views.BusinessLatLongViewset)

urlpatterns = [
    path(
        'accounts/password/reset/',
        PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'),
        name="password_reset"),
    path(
        'accounts/password/reset/done/',
        PasswordResetView.as_view(
            template_name='registration/password_reset_done.html'),
        name="password_reset_done"),
    path(
        'accounts/password/reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'),
        name="password_reset_confirm"),
    path(
        'accounts/password/done/',
        PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'),
        name="password_reset_complete"),
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path(
        'events-dropdown-select',
        views.event_list_preset,
        name='event_list_preset'),
    path('events/', views.event_list_text, name='event_list_text'),
    path('event/<slug>/', views.event_detail, name='event_detail'),
    path('business/', BusinessResultsListView.as_view(), name='business_list'),
    path('event/', EventResultsListView.as_view(), name='event_list'),
    path('business/<slug>/', views.business_detail, name='business_detail'),
    path('directory/', views.business_directory, name='business_directory'),
    path('events_directory/', views.event_directory, name='event_directory'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('my-profile/', views.get_user_profile, name="get_user_profile"),
    path(
        'review/<id>/delete',
        views.user_delete_review,
        name="user_delete_review"),
    url(r'(?P<id>\d+)/favorite_event/$',
        views.favorite_event,
        name='favorite_event'),
    path(
        'event/<int:pk>/favorite_event/',
        views.favorite_event,
        name='favorite_event'),
    path('mapboxTest', views.mapboxTest, name='mapboxTest'),
    path('mapBoxPlotTest', views.mapBoxPlotTest, name='mapBoxPlotTest'),
    path('api/', include('rest_framework.urls')),
    path('api/', include((router.urls, 'core'), namespace="api")),
    url(r'^api/(?P<pk>[0-9]+)/$', api_views.BusinessDetailViewset),
]
