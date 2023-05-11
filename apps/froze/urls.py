from django.urls import path, re_path
from apps.froze.views import index, FrozeAllView, FrozeUUIDView

urlpatterns = [
    path('', index, name='index'),
    path('frozes/all/', FrozeAllView.as_view(), name="frozes_all"),
    re_path(r'^frozes/(?P<uuid>\w+)/$', FrozeUUIDView.as_view(), name="froze_uuid"),
]
