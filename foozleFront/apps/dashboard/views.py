from django.views.generic import TemplateView, View, FormView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from foozleFront.apps.project.models import Project
from .forms import LoginForm, ChangePasswordForm


class Home(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data()
        context['projects'] = Project.objects.all()
        return context


class Login(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return super(Login, self).form_valid(form)


def logout_view(request):
    logout(request)
    return redirect("/")


class ChangePassword(FormView):
    template_name = 'change_password.html'
    form_class = ChangePasswordForm
    success_url = "/"

    def form_valid(self, form):
        password = form.cleaned_data["password"]
        user = self.request.user
        user.set_password(password)
        user.save()
        return super(ChangePassword, self).form_valid(form)
