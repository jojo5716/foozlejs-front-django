from django.conf.urls import url
from .views import HomeProject, RecentProject, IssueDetailProject, UrlProject, UrlDetailProject, CaptureError
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^(?P<id_project>[0-9]+)/$', HomeProject.as_view(), name="project_home"),
    url(r'^(?P<id_project>[0-9]+)/recent/$', RecentProject.as_view(), name="project_recent"),
    url(r'^(?P<id_project>[0-9]+)/issue/(?P<id_issue>[0-9]+)$', IssueDetailProject.as_view(), name="project_issue_detail"),
    url(r'^(?P<id_project>[0-9]+)/url/$', UrlProject.as_view(), name="project_url"),
    url(r'^(?P<id_project>[0-9]+)/url/detail/$', UrlDetailProject.as_view(), name="project_url_detail"),
    url(r'^capture$', csrf_exempt(CaptureError)),
]
