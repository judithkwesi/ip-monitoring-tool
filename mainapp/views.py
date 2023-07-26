#Telling django to render the views .html file

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages


# Create your views here. 

@login_required(login_url='login')
def dashboard(request):   #Main screen
    return render(request, 'registration/dashboard.html', {'section': 'dashboard'})

@login_required(login_url='login')
def users(request):
    return render(request, 'registration/users.html', {'section': 'users'})

@login_required(login_url='login')
def settings(request):
    return render(request, 'registration/settings.html', {'section': 'settings'})

@login_required(login_url='login')
def logout_user(request):
	logout(request)
	messages.success(request, ('Successful logged out!'))
        
	response = HttpResponse()
	response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	response['Pragma'] = 'no-cache'
	response['Expires'] = '0'
	return redirect('login')
