from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from foozleFront.apps.decorators.login import login_required

from .views import HomeProject, RecentProject, IssueDetailProject, UrlProject, UrlDetailProject, CaptureError
from foozleFront.apps.decorators.login import login_required

urlpatterns = [
    url(r'^(?P<id_project>[0-9]+)/$', login_required(HomeProject.as_view()), name="project_home"),
    url(r'^(?P<id_project>[0-9]+)/recent/$', login_required(RecentProject.as_view()), name="project_recent"),
    url(r'^(?P<id_project>[0-9]+)/issue/(?P<id_issue>[0-9]+)$', login_required(IssueDetailProject.as_view()), name="project_issue_detail"),
    url(r'^(?P<id_project>[0-9]+)/url/$', login_required(UrlProject.as_view()), name="project_url"),
    url(r'^(?P<id_project>[0-9]+)/url/detail/$', login_required(UrlDetailProject.as_view()), name="project_url_detail"),
    url(r'^capture$', csrf_exempt(login_required(CaptureError))),
]
