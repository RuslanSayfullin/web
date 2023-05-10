from django.urls import path, re_path

from apps.froze.views import index

urlpatterns = [
    path('', index, name='index'),
]
