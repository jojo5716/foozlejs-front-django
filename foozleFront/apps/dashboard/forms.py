from django import forms
from django.contrib.auth import authenticate, login

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
    	username = self.cleaned_data["username"]
    	password = self.cleaned_data["password"]
    	
    	user = authenticate(username=username, password=password)
    	if user is None:
    		 raise forms.ValidationError("Passwords don't match")
    		 
    	return password