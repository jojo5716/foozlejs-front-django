from django.conf.urls import url
from .views import HomeProject, RecentProject, IssueDetailProject

urlpatterns = [
    url(r'^(?P<id_project>[0-9]+)/$', HomeProject.as_view(), name="project_home"),
    url(r'^(?P<id_project>[0-9]+)/recent/$', RecentProject.as_view(), name="project_recent"),
    url(r'^(?P<id_project>[0-9]+)/issue/(?P<id_issue>[0-9]+)$', IssueDetailProject.as_view(), name="project_issue_detail"),
]
