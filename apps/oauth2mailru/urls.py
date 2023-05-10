from django.urls import path, re_path

from apps.oauth2mailru.views import MailruOAuthView, mailru_logout

app_name = "auth"
urlpatterns = [
    re_path(r'^mailru/$', MailruOAuthView.as_view(), name="login"),
    re_path(r'^mailru/logout/$', mailru_logout, name="logout"),
]