from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from foozleFront.apps.decorators.login import login_required
from .views import (HomeProject,
                    RecentProject,
                    IssueDetailProject,
                    UrlProject,
                    UrlDetailProject,
                    BrowserProject,
                    CaptureError,
                    InternalErrorView,
                    InternalErrorDetailView,
                    HowToInstall,
                    internal_api_error)

urlpatterns = [
    url(r'^(?P<id_project>[0-9]+)/$', login_required(HomeProject.as_view()), name="project_home"),
    url(r'^(?P<id_project>[0-9]+)/recent/$', login_required(RecentProject.as_view()), name="project_recent"),
    url(r'^(?P<id_project>[0-9]+)/issue/(?P<id_issue>[0-9]+)$', login_required(IssueDetailProject.as_view()), name="project_issue_detail"),
    url(r'^(?P<id_project>[0-9]+)/url/$', login_required(UrlProject.as_view()), name="project_url"),
    url(r'^(?P<id_project>[0-9]+)/url/detail/$', login_required(UrlDetailProject.as_view()), name="project_url_detail"),
    url(r'^(?P<id_project>[0-9]+)/browsers/$', login_required(BrowserProject.as_view()), name="project_browser"),
    url(r'^(?P<id_project>[0-9]+)/install/$', login_required(HowToInstall.as_view()), name="project_install"),
    url(r'^capture$', csrf_exempt(CaptureError)),
    url(r'^internal/error/$', internal_api_error, name="foozle_internal_error"),
    url(r'^internal/errors/list$', login_required(InternalErrorView.as_view()), name="foozle_internal_error_list"),
    url(r'^internal/errors/(?P<id_error>[0-9]+)', login_required(InternalErrorDetailView.as_view()), name="foozle_internal_error_detail"),

]
