#This will have codes for the login form

from django import forms

class LoginForm(forms.Form):
    #creates a character field to accept text input from users. The required=True parameter specifies that the field is mandatory,
    #sets the minimum length of the username to 3 characters.
    username = forms.CharField(required=True, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})) 
    
    #creates a character field to accept text input.
    #Masks password characters for security reasons. 
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))