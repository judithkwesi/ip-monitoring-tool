import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.core.cache import cache
from .forms import MySelectForm, AddUserForm, AddIPForm
import ipaddress
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from .models import IPSpace


@never_cache
def login_view(request):
     if request.user.is_authenticated:
          return HttpResponseRedirect('/')
     
     if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Successfully logged in")
            cache.delete(f'login_attempts:{request.META.get("REMOTE_ADDR")}')
            return redirect('dashboard')
        else:
            handle_invalid_login_attempt(request, form)

     return render(request, 'registration/login.html', {})


@login_required(login_url='login')
def dashboard(request):
     all_ips = IPSpace.objects.all()
     renu_ips = [ip_obj.ip_space for ip_obj in all_ips]

     blocklist = []
     blacklisted_cins = []
     blacklisted_blocklist = []
     blacklisted_spamhaus = []

     with open('./mainapp/sites/cins.txt', 'r') as file:
               for line in file.readlines():
                    ip_address = ipaddress.ip_address(line.strip())
                    for entry in renu_ips:
                         if ip_address in ipaddress.ip_network(entry):
                              blocklist.append({"ip": str(ip_address), "source": "CINS"})

     with open('./mainapp/sites/blocklist.txt', 'r') as file:
               for line in file.readlines():
                    ip_address = ipaddress.ip_address(line.strip())
                    for entry in renu_ips:
                         if ip_address in ipaddress.ip_network(entry):
                              blocklist.append({"ip": str(ip_address), "source": "Blocklist"})

     if request.method == 'POST':
          form = MySelectForm(request.POST)
          if form.is_valid():
               selected_option = form.cleaned_data['select_choice']

               selected_option_label = dict(form.fields['select_choice'].choices).get(selected_option)
               # Render the same template with updated options

               blocklist_json = json.dumps(blocklist)

               context = {
                    "blocklist": blocklist_json,
                    'section': 'dashboard',
                    'form': form,
                    'selected_option': selected_option,
                    'selected_label': selected_option_label,
                    'blacklisted_cins': blacklisted_cins,
               }

               return render(request, 'registration/dashboard.html', context)
     else:
          form = MySelectForm(initial={'select_choice': 'option1'})
          selected_option = form.initial['select_choice']

          selected_option_label = dict(form.fields['select_choice'].choices).get(selected_option)

          blocklist_json = json.dumps(blocklist)

          context = {
               "blocklist": blocklist_json,
               'section': 'dashboard',
               'form': form,
               'selected_option': selected_option,
               'selected_label': selected_option_label,
               'blacklisted_cins': blacklisted_cins,
          }


          return render(request, 'registration/dashboard.html', context)

@login_required(login_url='login')
def add_ip_space(request):
     if request.method == 'POST':
          form = AddIPForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request, f"Successfully added IP space")
               return HttpResponseRedirect('/')
          else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{error}")

            return HttpResponseRedirect('/')
     form = AddIPForm() 

@login_required(login_url='login')
def add_user(request):
     if request.method == 'POST':
          form = AddUserForm(request.POST)
          print(request) 
          if form.is_valid():
               form.save()
               messages.success(request, "Successfully added user")
               return HttpResponseRedirect('/users')
          else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{error}")

            return HttpResponseRedirect('/users')
     form = AddUserForm() 
     

@login_required(login_url='login')
def users(request):
    users = User.objects.all()
    usernames_list = [{"username": user.username, "access_level": user.is_superuser} for user in users]
    data = {"users": usernames_list}
    context = {
         "users": json.dumps(data),
         "section": "users"
    }
    return render(request, 'registration/users.html', context)

@login_required(login_url='login')
def settings(request):
    return render(request, 'registration/settings.html', {'section': 'settings'})

@login_required(login_url='login')
def logout_user(request):
    request.session.flush()
    logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect('/')


def handle_invalid_login_attempt(request, form):
    user_ip = request.META.get('REMOTE_ADDR')
    key = f'login_attempts:{user_ip}'
    attempts = cache.get(key, 0)
    MAX_LOGIN_ATTEMPTS_PER_HOUR = 5

    if attempts >= MAX_LOGIN_ATTEMPTS_PER_HOUR:
        messages.error(request, "Too many failed login attempts. Try again later.")
        return HttpResponseForbidden("<h1>403 Forbidden.</h1><p>Too many failed login attempts. Try again later.</p>")
    else:
        cache.set(key, attempts + 1, 3600)
        messages.error(request, "Invalid username or password.")

    return redirect('login')
