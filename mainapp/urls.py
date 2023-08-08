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

    # # password reset
    # path('password_reset/', never_cache(auth_views.PasswordResetView.as_view()), name='password_reset'),
    # path('password_reset/done/', never_cache(auth_views.PasswordResetDoneView.as_view()), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', never_cache(auth_views.PasswordResetConfirmView.as_view()), name='password_reset_confirm'),
    # path('reset/done/', never_cache(auth_views.PasswordResetCompleteView.as_view()), name='password_reset_complete'),

    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),


    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='registratio/password_reset_complete.html'),name='password_reset_complete'),


]


