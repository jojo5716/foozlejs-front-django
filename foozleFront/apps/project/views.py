import json
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Project, Error


class HomeProject(TemplateView):
    template_name = 'project/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(HomeProject, self).get_context_data()

        context['errors'] = Error.objects.filter(project=kwargs['id_project'],
                                                 resolved=False).order_by('-id')[:3]
        context['project'] = kwargs['id_project']
        return context


class RecentProject(TemplateView):
    template_name = 'project/recent.html'

    def get_context_data(self, **kwargs):
        context = super(RecentProject, self).get_context_data()


        context['project_id'] = 1
        context["errors"] = Error.objects.filter(project=1)

        return context


class IssueDetailProject(TemplateView):
    template_name = 'project/issue_detail.html'


def CaptureError(request):
    token = request.GET.get('token')
    if request.body and token:
        try:
            project = Project.objects.get(token=token, active=True)
        except Project.DoesNotExist:
            raise
        else:
            error = Error()
            error.project = project
            error.data = json.loads(request.body)
            error.save()

            response = HttpResponse(json.dumps({"ok": True}))
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"

            return response
