#This will have codes for the login form

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import IPSpace, SyncInterval
from ipaddress import ip_network, AddressValueError

class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})) 
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

class SyncIntervalForm(forms.ModelForm):
    sync_interval = forms.CharField(required=True, min_length=1, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))

    class Meta:
        model = SyncInterval
        fields = ['sync_interval']

class AddIPForm(forms.ModelForm):
    ip_space = forms.CharField(required=True, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})) 
    description = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

    class Meta:
        model = IPSpace
        fields = ['ip_space', 'description']

    def clean_ip_space(self):
        ip_space = self.cleaned_data.get('ip_space')
        
        try:
            ip_network(ip_space)  # This will raise an exception if the IP range is invalid
        except (AddressValueError, ValueError) as e:
            raise forms.ValidationError("Invalid IP address range.")
        
        return ip_space

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