#This will have codes for the login form

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})) 
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

class AddIPForm(forms.Form):
    ip_space = forms.CharField(required=True, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})) 
    description = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

class AddUserForm(UserCreationForm):
    username = forms.CharField(required=True, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})) 
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

# Selectbox on the dashboard
class MySelectForm(forms.Form):
    OPTIONS = [
        ('option1', 'All Databases'),
        ('option2', 'Spamhaus'),
        ('option3', 'Blocklist'),
        ('option4', 'CINS'),
        ('option5', 'AbuselIPDB'),
    ]
    
    select_choice = forms.ChoiceField(choices=OPTIONS, widget=forms.Select(attrs={'class': 'form-control'}))