from django.views.generic import TemplateView, View

from foozleFront.apps.project.models import Project


class Home(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data()
        context['projects'] = Project.objects.all()
        return context


class Login(TemplateView):
    template_name = 'login.html'


class Logout(View):
    pass