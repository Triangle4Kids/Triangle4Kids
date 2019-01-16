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
# from django.views.generic import TemplateView
# from core.views import EventListView
# from core.views import search
from core import views
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

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
    path('business/', views.business_directory, name='business_directory'),
    path('business/<slug>/', views.business_detail, name='business_detail'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('my-profile/', views.get_user_profile, name="get_user_profile"),
    path(
        'review/<id>/delete',
        views.user_delete_review,
        name="user_delete_review"),
    path(
        r'(?P<id>\d+)/favorite_event/$',
        views.favorite_event,
        name='favorite_event'),
    path(
        'event/<int:pk>/favorite_event/',
        views.favorite_event,
        name='favorite_event'),
    path('mapboxTest', views.mapboxTest, name='mapboxTest'),
    path('mapBoxPlotTest', views.mapBoxPlotTest, name='mapBoxPlotTest'),
]
