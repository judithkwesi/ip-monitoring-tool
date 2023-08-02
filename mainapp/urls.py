from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login_view, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page=None), name='logout'), 
    path('logout/', views.logout_user, name='logout'),
    path('add_user/', views.add_user, name='add_user'),
    
    # password change
    path('password_change/', login_required(login_url='login')(auth_views.PasswordChangeView.as_view()), name='password_change'),
    path('password_change/done/', login_required(login_url='login')(auth_views.PasswordChangeDoneView.as_view()), name='password_change_done'), 

]