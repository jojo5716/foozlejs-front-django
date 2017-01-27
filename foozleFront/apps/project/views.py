import json

from PIL import Image
from django import http

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Max, Min
from .models import Project, Error, InternalErrors
from ..utils.charts import chart_by_top_browser
from ..utils.browser import get_browser_from_useragent


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
        browser = get_browser_from_useragent(error.data['environment']['userAgent'])

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
                data[url] = {"errors": 0, "lastView": error.timestamp}

            data[url]["errors"] += 1

            if error.timestamp >= data[url]["lastView"]:
                data[url]["lastView"] = error.timestamp

        return data


class UrlDetailProject(TemplateView):
    template_name = "project/url_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UrlDetailProject, self).get_context_data()

        url = self.request.GET.get("url")
        project = get_project_by_id(kwargs['id_project'])
        errors = project.error_set.filter(data__url=url)

        context['url'] = url
        context['project'] = project
        context['errors_seen'] = errors.aggregate(Min("timestamp"), Max("timestamp"))
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


class BrowserProject(TemplateView):
    template_name = 'project/browser.html'

    def get_context_data(self, **kwargs):
        context = super(BrowserProject, self).get_context_data()

        errors = Error.objects.filter(project=kwargs["id_project"]).order_by('-id')
        context["browsers"] = self.get_browsers(errors)
        context['project'] = get_project_by_id(kwargs['id_project'])
        context['errors'] = self.get_errors(errors)

        return context

    def get_browsers(self, errors):
        data = {}
        for error in errors:
            browser = get_browser_from_useragent(error.data['environment']['userAgent'])

            if browser not in data:
                data[browser] = 0

            data[browser] += 1

        return data

    def get_errors(self, errors):
        data = {}
        errors_count = {}

        for error in errors:
            browser = get_browser_from_useragent(error.data['environment']['userAgent'])
            message = error.data["message"]

            if message not in data:
                data[message] = []
                errors_count[browser] = 0

            errors_count[browser] += 1

            data[message].append({
                "browser": browser,
                "errors": errors_count
            })

        return data


def get_project_by_id(project_id, active=True):
    try:
        return Project.objects.get(id=project_id, active=active)
    except Project.DoesNotExist:
        return None


def internal_api_error(request):
    token = request.GET.get('token')

    response = HttpResponse(content_type="image/jpeg")
    img = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
    img.save(response, 'JPEG')

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    if request.GET and token:
        error = InternalErrors(data=dict(request.GET))
        error.save()

    return response


class InternalErrorView(TemplateView):
    template_name = "project/internal_errors.html"

    def get_context_data(self, **kwargs):
        context = super(InternalErrorView, self).get_context_data()
        context["errors"] = InternalErrors.objects.all().order_by('-id')
        return context


class InternalErrorDetailView(TemplateView):
    template_name = "project/internal_error_detail.html"

    def get_context_data(self, **kwargs):
        context = super(InternalErrorDetailView, self).get_context_data()

        try:
            context["error"] = InternalErrors.objects.get(id=kwargs['id_error'])
        except Exception:
            pass

        return context


class HowToInstall(TemplateView):
    template_name = "project/install.html"

    def get_context_data(self, **kwargs):
        context = super(HowToInstall, self).get_context_data()
        try:
            context["project"] = Project.objects.get(id=kwargs["id_project"])
        except Project.DoesNotExist:
            raise http.Http404()
        return context
