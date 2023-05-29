from django.urls import path, include
from rest_framework import routers

from apps.api.views import FrozeAPICreate, FrozeAndDogovorIndiView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v0/froze-create/', FrozeAPICreate.as_view()),
    path('api/v1/froze-create/', FrozeAndDogovorIndiView.as_view()),
]
