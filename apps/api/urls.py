from django.urls import path
from apps.api.views import FrozeAPICreate

urlpatterns = [
    path('api/v1/froze-create/', FrozeAPICreate.as_view()),
]
