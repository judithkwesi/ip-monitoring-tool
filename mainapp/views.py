import json
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.core.cache import cache
from .forms import MySelectForm, AddUserForm, AddIPForm, SyncIntervalForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from .models import IPSpace, SyncInterval
from mainapp.utils.utils import generateContext, handle_invalid_login_attempt, check_file, get_device_info
from mainapp.utils.custom_decorators import custom_admin_only, custom_authorised_user
import logging
from user_agents import parse
from django.views.decorators.csrf import csrf_exempt
import subprocess
from .check_for_renu_ip import identify_blacklisted_ip_addresses
from django.contrib.auth import views as auth_views



logger = logging.getLogger('ip-monitoring-tool')

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@never_cache
def login_view(request):
     user_ip = get_user_ip(request)
     device_info = get_device_info(request)
     if request.user.is_authenticated:
          return HttpResponseRedirect('/')
     if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f"200 OK {user_ip} {user} {request.path} {device_info}")
            messages.success(request, "Successfully logged in")
            cache.delete(f'login_attempts:{request.META.get("REMOTE_ADDR")}')
            return redirect('dashboard')
        else:
            handle_invalid_login_attempt(request)

     return render(request, 'registration/login.html', {})


@custom_authorised_user
def dashboard(request):
     all_ips = IPSpace.objects.all()
     renu_ips = [ip_obj.ip_space for ip_obj in all_ips]
     blocklist = []

     check_file('./mainapp/sites/cins.txt', renu_ips, blocklist, "CINS")
     check_file('./mainapp/sites/blocklist.txt', renu_ips, blocklist, "Blocklist")

     for ip_space in renu_ips:
         if ":" in ip_space:
             identify_blacklisted_ip_addresses('./mainapp/sites/spamhausv6.txt', ip_space, blocklist, "Spamhaus")
         else:
             identify_blacklisted_ip_addresses('./mainapp/sites/spamhaus.txt', ip_space, blocklist, "Spamhaus")

     for ip_space in renu_ips:
         if ":" in ip_space:
             identify_blacklisted_ip_addresses('./mainapp/sites/spamhausv6.txt', ip_space, blocklist, "Spamhaus")
         else:
             identify_blacklisted_ip_addresses('./mainapp/sites/spamhaus.txt', ip_space, blocklist, "Spamhaus")

     sorted_data = sorted(blocklist, key=lambda x: x['ip'])

     if request.method == 'POST':
          form = MySelectForm(request.POST)
          if form.is_valid():
               selected_option = form.cleaned_data['select_choice']
               context = generateContext(selected_option, sorted_data, form)

               return render(request, 'registration/dashboard.html', context)
     else:
          form = MySelectForm(initial={'select_choice': 'option1'})
          selected_option = form.initial['select_choice']
          context = generateContext(selected_option, sorted_data, form)

          return render(request, 'registration/dashboard.html', context)
     

@login_required(login_url='login')
def add_ip_space(request):
     user_ip = get_user_ip(request)
     device_info = get_device_info(request)
     username = request.user.username if request.user.is_authenticated else "Anonymous"
     if request.method == 'POST':
          form = AddIPForm(request.POST)
          if form.is_valid():
               form.save()
               logger.info(f"200 OK {user_ip} {username} {request.path} {device_info}")
               messages.success(request, f"Successfully added IP space")
               return HttpResponseRedirect('/')
          else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{error}")
                     logger.info(f"Failed to add IP space: {error}")
            logger.error(f"400 Bad request {user_ip} {username} {request.path} {device_info}")

            return HttpResponseRedirect('/')
     form = AddIPForm() 

@custom_admin_only
def add_user(request):
     user_ip = get_user_ip(request)
     device_info = get_device_info(request)
     username = request.user.username if request.user.is_authenticated else "Anonymous"
     if request.method == 'POST':
          form = AddUserForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request, "Successfully added user")
               logger.info(f"200 OK {user_ip} {username} {request.path} {device_info}")
               return HttpResponseRedirect('/users')
          else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{error}")
            logger.error(f"400 Bad request {user_ip} {username} {request.path} {device_info}")

            return HttpResponseRedirect('/users')
     form = AddUserForm()


@custom_admin_only
def update_sync_interval(request):
     user_ip = get_user_ip(request)
     device_info = get_device_info(request)
     username = request.user.username if request.user.is_authenticated else "Anonymous"
     if request.method == 'POST':
          form = SyncIntervalForm(request.POST)

          if form.is_valid():
               form.save()
               messages.success(request, "Successfully updated Sync Interval")
               logger.info(f"200 OK {user_ip} {username} {request.path} {device_info}")
               return HttpResponseRedirect('/settings')
          else:
            for _, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{error}")
            logger.error(f"400 Bad Request {user_ip} {username} {request.path} {device_info}")

            return HttpResponseRedirect('/settings')

     return HttpResponseRedirect('/settings')


@custom_admin_only
def users(request):
    users = User.objects.all()
    usernames_list = [{"username": user.username, "access_level": user.is_superuser} for user in users]
    data = {"users": usernames_list}
    context = {
         "users": json.dumps(data),
         "section": "users"
    }
    return render(request, 'registration/users.html', context)


@custom_admin_only
def settings(request):
     sync = SyncInterval.objects.all()
     sync_intervals = [ip_obj.sync_interval for ip_obj in sync]

     if sync_intervals:
          sync_interval = int(sync_intervals[-1])
     else:
          sync_interval = 12

     context = {
          "section": "settings",
          "sync_interval": sync_interval
     }
     return render(request, 'registration/settings.html', context)


@login_required(login_url='login')
def logout_user(request):
    user_ip = get_user_ip(request)
    device_info = get_device_info(request)
    username = request.user.username if request.user.is_authenticated else "Anonymous"
    logger.info(f"200 OK {user_ip} {username} {request.path} {device_info}")
    logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect('/')




# Password Reset View
@never_cache
def password_reset(request):
    return auth_views.PasswordResetView.as_view()(request)

# Password Reset Done View
@never_cache
def password_reset_done(request):
    return auth_views.PasswordResetDoneView.as_view()(request)

# Password Reset Confirm View
@never_cache
def password_reset_confirm(request, uidb64, token):
    return auth_views.PasswordResetConfirmView.as_view()(request, uidb64=uidb64, token=token)

# Password Reset Complete View
@never_cache
def password_reset_complete(request):
    return auth_views.PasswordResetCompleteView.as_view()(request)
@csrf_exempt
def github_webhook(request):
     if request.method == 'POST':
          payload = json.loads(request.body)
          event_type = request.headers.get('X-GitHub-Event')

          if event_type == 'push' and 'ref' in payload and payload['ref'] == 'refs/heads/staging':
              author_name = payload['pusher']['name']
              commit_message = payload['head_commit']['message']
              logger.info(f"Attempt to deployment: {author_name} - {commit_message} /{payload['ref']}")
              try:
                  subprocess.run(['/usr/bin/sudo', '/home/charles/ip-reputation/staging/ip-monitoring-tool/.github/workflows/deploy.sh'])
                  logger.info(f"Deployment: {author_name} - {commit_message} /{payload['ref']}")
              except subprocess.CalledProcessError as e:
                  logger.error(f"Error deploying from {author_name}/ {commit_message}: {e}")
              

     return HttpResponse(status=200)
