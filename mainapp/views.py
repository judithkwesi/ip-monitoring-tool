#Telling django to render the views .html file

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.views import LogoutView


# Create your views here. 

@login_required(login_url='login')
def dashboard(request):   #Main screen
    return render(request, 'registration/dashboard.html', {'section': 'dashboard'})


# class CustomLogoutView(LogoutView):
#     def dispatch(self, request, *args, **kwargs):
#         response = super().dispatch(request, *args, **kwargs)
#         # Set HTTP headers to prevent caching
#         response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#         response['Pragma'] = 'no-cache'
#         response['Expires'] = '0'
#         return response

#     def get_next_page(self):
#         # Redirect to the login page after logout
#         return '/login/'  # Replace '/login/' with the URL for your login view

@login_required(login_url='login')
def logout_user(request):
	logout(request)
	messages.success(request, ('Successful logged out!'))
        
	response = HttpResponse()
	response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	response['Pragma'] = 'no-cache'
	response['Expires'] = '0'
	return redirect('login')
