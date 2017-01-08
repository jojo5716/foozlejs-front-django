from django.conf.urls import url
from .views import Home, Login, Logout
from foozleFront.apps.decorators.login import login_required


urlpatterns = [
    url(r'^$', login_required(Home.as_view()), name="home"),
    url(r'^login/$', Login.as_view(), name="login"),
    url(r'^logout/$', Logout.as_view(), name="logout"),
]
