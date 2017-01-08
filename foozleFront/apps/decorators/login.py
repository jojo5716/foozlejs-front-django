from django.conf import settings
from django.http import HttpResponseRedirect


def login_required(view):
    def f(request, *args, **kwargs):
    	print request.user.is_anonymous()
        if request.user.is_anonymous():
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return view(request, *args, **kwargs)
    return f