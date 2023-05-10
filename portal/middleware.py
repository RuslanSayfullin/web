from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(i in path for i in ["/auth/", "/admin/", "/api/", "/media/"]):
                return HttpResponseRedirect(reverse(settings.LOGIN_URL))

        if not request.user.is_active:
            logout(request)

        response = self.get_response(request)
        return response
