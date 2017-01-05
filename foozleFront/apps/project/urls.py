from django.conf.urls import url
from .views import HomeProject

urlpatterns = [
    url(r'^project/(?P<id_test>[0-9]+)/$', HomeProject.as_view(), name="project_home"),
]
