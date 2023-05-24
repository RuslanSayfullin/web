from django.urls import path, re_path

from apps.dogovora.views import CreateUpdateDogovorIndi, nomer_dogovora, drugoy_dogovor

app_name = 'dogovora'
urlpatterns = [
    re_path(r'^nomer_dogovora$', nomer_dogovora, name="nomer_dogovora"),
    re_path(r'^drugoy_dogovor$', drugoy_dogovor, name="drugoy_dogovor"),
    re_path(r'^(?P<froze_uuid>\w+)$', CreateUpdateDogovorIndi.as_view(), name="create_update_indi"),
]
