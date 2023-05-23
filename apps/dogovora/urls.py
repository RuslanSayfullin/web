from django.urls import path, re_path, include

from apps.dogovora.views import CreateUpdateDogovorIndi

app_name = 'dogovora'
urlpatterns = [
    re_path(r'^(?P<froze_uuid>\w+)$', CreateUpdateDogovorIndi.as_view(), name="create_update_indi"),
]
