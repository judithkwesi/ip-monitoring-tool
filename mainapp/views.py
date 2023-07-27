from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.cache import cache
from .forms import MySelectForm
# from django_ratelimit.decorators import ratelimit

# Create your views here. 
# @ratelimit(key='ip', rate='5/h', block=True)
def login_view(request):
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
    if request.method == 'POST':
        form = MySelectForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['select_choice']

            selected_option_label = dict(form.fields['select_choice'].choices).get(selected_option)
            # Render the same template with updated options
            return render(request, 'registration/dashboard.html', {'section': 'dashboard', 'form': form, 'selected_option': selected_option, 'selected_label': selected_option_label})
    else:
        form = MySelectForm(initial={'select_choice': 'option1'})
        selected_option = form.initial['select_choice']

        selected_option_label = dict(form.fields['select_choice'].choices).get(selected_option)

        return render(request, 'registration/dashboard.html', {'section': 'dashboard', 'form': form, 'selected_option': selected_option, 'selected_label': selected_option_label})

    return render(request, 'registration/dashboard.html', {'section': 'dashboard', 'form': ""})

@login_required(login_url='login')
def users(request):
    users = User.objects.all()
    return render(request, 'registration/users.html', {'users': users, 'section': 'users'})

@login_required(login_url='login')
def settings(request):
    return render(request, 'registration/settings.html', {'section': 'settings'})

@login_required(login_url='login')
def logout_user(request):
	logout(request)
        
	response = HttpResponse()
	response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	response['Pragma'] = 'no-cache'
	response['Expires'] = '0'
	return redirect('login')


@login_required(login_url='login')
def logout_user(request):
	logout(request)
        
	response = HttpResponse()
	response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	response['Pragma'] = 'no-cache'
	response['Expires'] = '0'
	return redirect('login')

