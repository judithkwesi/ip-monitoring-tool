#This will have codes for the login form

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=3) 
    password = forms.CharField(widget=forms.PasswordInput)