from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.contrib.auth.views import (
    
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_user, name='logout'),
    path('add_user/', views.add_user, name='add_user'),
    path('sync_interval/', views.update_sync_interval, name='sync_interval'),
    path('add_ip_space/', views.add_ip_space, name='add_ip_space'),
    
    # password change
    path('password_change/', login_required(login_url='login')(auth_views.PasswordChangeView.as_view()), name='password_change'),
    path('password_change/done/', login_required(login_url='login')(auth_views.PasswordChangeDoneView.as_view()), name='password_change_done'), 
]
