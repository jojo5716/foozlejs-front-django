from django import forms
from django.contrib.auth import authenticate


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


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data["password"]
        repeat_password = self.cleaned_data["repeat_password"]

        if password != repeat_password:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data


class NewProjectForm(forms.Form):
    name = forms.CharField()
