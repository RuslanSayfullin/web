from django.urls import path, re_path, include

urlpatterns = [
    path('', include('apps.api.urls')),
    path('', include('apps.froze.urls')),
    re_path(r'^auth/', include('apps.oauth2mailru.urls', namespace="auth")),
    re_path(r'^search/', include('apps.search.urls', namespace="search")),
    re_path(r'^dogovora/', include('apps.dogovora.urls', namespace='dogovora')),
]
