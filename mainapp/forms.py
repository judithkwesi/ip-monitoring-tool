#This will have codes for the login form

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})) 
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

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