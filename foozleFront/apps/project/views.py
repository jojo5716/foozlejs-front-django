import json
import httpagentparser
from datetime import datetime
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Project, Error
from ..utils.charts import chart_by_top_browser

class HomeProject(TemplateView):
    template_name = 'project/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(HomeProject, self).get_context_data()

        self.errors = Error.objects.filter(project=kwargs['id_project']).order_by('-id')

        context['errors'] = self.errors.filter(resolved=False)[:6]

        context['project'] = get_project_by_id(kwargs['id_project'])

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
        context['project'] = get_project_by_id(kwargs['id_project'])

        return context


class IssueDetailProject(TemplateView):
    template_name = 'project/issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super(IssueDetailProject, self).get_context_data()

        context['project'] = get_project_by_id(kwargs['id_project'])

        try:
            context["error"] = Error.objects.get(project=kwargs['id_project'],
                                                id=kwargs['id_issue'])
        except Error.DoesNotExist:
            pass

        return context


class UrlProject(TemplateView):
    template_name = "project/url.html"

    def get_context_data(self, **kwargs):
        context = super(UrlProject, self).get_context_data()

        project = get_project_by_id(kwargs['id_project'])

        context['project'] = project
        context['errors'] = self.get_errors_url(project.error_set.filter(resolved=False))

        return context

    def get_errors_url(self, errors):
        data = {}

        for error in errors:
            url = error.data["url"]

            if url not in data:
                data[url] = { "errors": 0, "lastView": error.timestamp}

            data[url]["errors"] += 1

            if error.timestamp >= data[url]["lastView"]:
                data[url]["lastView"] = error.timestamp

        return data


class UrlDetailProject(TemplateView):
    template_name = "project/url_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UrlDetailProject, self).get_context_data()

        project = get_project_by_id(kwargs['id_project'])
        errors = project.error_set.filter(data__url=self.request.GET.get("url"))

        context['project'] = project
        context['errors'] = errors.order_by('-timestamp')
        context['chart_urls'] = self.get_errors(errors)
        context['chart_browsers'] = chart_by_top_browser(errors)

        return context

    def get_errors(self, errors):
        data = {}
        for error in errors:
            timestamp = error.data["timestamp"].split("T")[0]

            if timestamp not in data:
                data[timestamp] = {"errors": 0}

            data[timestamp]["errors"] += 1

        return data


def CaptureError(request):
    token = request.GET.get('token')
    success = True

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

        response = HttpResponse(json.dumps({"success": success}))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response

def get_project_by_id(project_id, active=True):
    try:
        return Project.objects.get(id=project_id, active=active)
    except Project.DoesNotExist:
        return None