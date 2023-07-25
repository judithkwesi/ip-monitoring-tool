#Telling django to render the views .html file

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages


# Create your views here. 

@login_required(login_url='login')
def dashboard(request):   #Main screen
    return render(request, 'registration/dashboard.html', {'section': 'dashboard'})


@login_required(login_url='login')
def logout_user(request):
	logout(request)
	messages.success(request, ('Successful logged out!'))
	return redirect('login')
