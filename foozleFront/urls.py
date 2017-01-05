from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('foozleFront.apps.dashboard.urls')),
    url(r'^project/', include('foozleFront.apps.project.urls'))
]

urlpatterns += [
    url(r'^static/(?P<path>.*)$', views.serve),
]
