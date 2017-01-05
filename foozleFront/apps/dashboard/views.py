from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data()
        context['id_test'] = 1
        return context
