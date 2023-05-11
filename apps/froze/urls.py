from django.urls import path, re_path
from apps.froze.views import index, FrozeAllView

urlpatterns = [
    path('', index, name='index'),
    path('frozes/all/', FrozeAllView.as_view(), name="frozes_all"),
]
