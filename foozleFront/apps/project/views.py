from django.views.generic import TemplateView


class HomeProject(TemplateView):
    template_name = 'project/dashboard.html'
