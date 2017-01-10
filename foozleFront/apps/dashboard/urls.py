from django.conf.urls import url
from .views import Home, Login, logout_view, ChangePassword
from foozleFront.apps.decorators.login import login_required


urlpatterns = [
    url(r'^$', login_required(Home.as_view()), name="home"),
    url(r'^login/$', Login.as_view(), name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^change/password/$', ChangePassword.as_view(), name="change_password"),
]
