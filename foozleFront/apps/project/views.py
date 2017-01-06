import json
import httpagentparser
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Project, Error


class HomeProject(TemplateView):
    template_name = 'project/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(HomeProject, self).get_context_data()

        self.errors = Error.objects.filter(project=kwargs['id_project']).order_by('-id')

        context['errors'] = self.errors.filter(resolved=False)[:6]

        context['project'] = kwargs['id_project']

        chart_browser, chart_urls = self.get_charts()
        context['chart_browser'] = chart_browser
        context['chart_urls'] = chart_urls

        return context


    def get_charts(self):
        browsers =  {}
        urls = {}

        for error in self.errors:
            self.get_errors_by_browser(error, browsers)
            self.get_errors_by_url(error, urls)

        return browsers, urls

    def get_errors_by_browser(self, error, dic):
        browser = httpagentparser.simple_detect(error.data['environment']['userAgent'])[1]

        if browser not in dic:
            dic[browser] = 0

        dic[browser] += 1

        return dic

    def get_errors_by_url(self, error, urls):
        url = error.data['url']

        if url not in urls:
            urls[url] = {'resolved': 0, 'unresolved': 0}

        if error.resolved:
            urls[url]['resolved'] += 1
        else:
            urls[url]['unresolved'] += 1


class RecentProject(TemplateView):
    template_name = 'project/recent.html'

    def get_context_data(self, **kwargs):
        context = super(RecentProject, self).get_context_data()

        context["errors"] = Error.objects.filter(project=kwargs["id_project"]).order_by('-id')

        return context


class IssueDetailProject(TemplateView):
    template_name = 'project/issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super(IssueDetailProject, self).get_context_data()

        context["error"] = Error.objects.get(project=kwargs['id_project'],
                                             id=kwargs['id_issue'])

        return context

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
