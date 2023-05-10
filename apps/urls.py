from django.urls import path, re_path, include

urlpatterns = [
    path('', include('apps.api.urls')),
    path('', include('apps.froze.urls')),
    re_path(r'^auth/', include('apps.oauth2mailru.urls', namespace="auth")),
]
