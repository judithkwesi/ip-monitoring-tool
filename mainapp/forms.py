#This will have codes for the login form

from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField() 
    password = form.CharField(widget=forms.PasswordInput)