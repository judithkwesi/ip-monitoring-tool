import json
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.cache import cache
from .forms import MySelectForm
import ipaddress
from django.views.decorators.cache import never_cache
# from django_ratelimit.decorators import ratelimit

# Create your views here. 
# @ratelimit(key='ip', rate='5/h', block=True)
@never_cache
def login_view(request):
      if request.user.is_authenticated:
          return HttpResponseRedirect('/')
      
      if request.method == 'POST':
        user_ip = request.META.get('REMOTE_ADDR')
        key = f'login_attempts:{user_ip}'
        attempts = cache.get(key, 0)

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            cache.delete(key)
            login(request, user)
            return redirect('dashboard')
        else:
             if attempts >= 5:  # Limiting to 5 login attempts per hour
                  print("Too many login attempts. Try again later.")
                  return HttpResponseForbidden("<h1>403 Forbidden.</h1><p>Too many failed login attempts. Try again later.</p>")
             else:
                  if(username):
                       cache.set(key, attempts + 1, 3600)
                       return redirect('login')
            
      else:
        return render(request, 'registration/login.html', {})

@login_required(login_url='login')
def dashboard(request):   #Main screen
    renu_ips = ['196.43.128.0/18', '137.63.128.0/17', '102.34.0.0/16', '2.56.192.0/22']

    blocklist = []
    blacklisted_cins = []
    blacklisted_blocklist = []
    blacklisted_spamhaus = []

    with open('./mainapp/sites/cins.txt', 'r') as file:
            # lines = file.readlines()
            # blocklist.append(lines)
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

    # blocklist = [ip.strip() for ip in blocklist[0]]

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

    # return render(request, 'registration/dashboard.html', {'section': 'dashboard', 'form': "", 'blocklist' : blocklist,})

@login_required(login_url='login')
def users(request):
    users = User.objects.all()
    # users_json = json.dump(users)
    usernames_list = [{"username": user.username, "access_level": user.is_superuser} for user in users]
    data = {"users": usernames_list}
    print(json.dumps(data))
    context = {
         "users": json.dumps(data),
         "section": "users"
    }
    return render(request, 'registration/users.html', context)

@login_required(login_url='login')
def settings(request):
    return render(request, 'registration/settings.html', {'section': 'settings'})

# @login_required(login_url='login')
# def logout_user(request):
#     logout(request)
#     request.session.clear()
#     return redirect('login')


@login_required(login_url='login')
def logout_user(request):
    request.session.flush()
    logout(request)

    # response = HttpResponse()
    # response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	# response['Pragma'] = 'no-cache'
	# response['Expires'] = '0'
    return HttpResponseRedirect('/')

