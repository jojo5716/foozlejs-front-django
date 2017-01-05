from django.views.generic import TemplateView


class HomeProject(TemplateView):
    template_name = 'project/dashboard.html'


class RecentProject(TemplateView):
    template_name = 'project/recent.html'

    def get_context_data(self, **kwargs):
        context = super(RecentProject, self).get_context_data()

        context['project_id'] = 1

        return context


class IssueDetailProject(TemplateView):
    template_name = 'project/issue_detail.html'

