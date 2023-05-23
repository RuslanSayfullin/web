from django.urls import path
from apps.api.views import FrozeAPICreate, FrozeAndDogovorIndiView

urlpatterns = [
    path('api/v1/froze-create/', FrozeAPICreate.as_view()),
    path('api/v2/froze-create/', FrozeAndDogovorIndiView.as_view()),
]
