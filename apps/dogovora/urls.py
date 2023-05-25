from django.urls import path, re_path

from apps.dogovora.views.create_dogovor import nomer_dogovora, drugoy_dogovor, CreateUpdateDogovorIndi
from apps.dogovora.views.print_dogovor import dogovor_main_view

app_name = 'dogovora'
urlpatterns = [
    re_path(r'^nomer_dogovora$', nomer_dogovora, name="nomer_dogovora"),
    re_path(r'^drugoy_dogovor$', drugoy_dogovor, name="drugoy_dogovor"),
    re_path(r'^(?P<froze_uuid>\w+)$', CreateUpdateDogovorIndi.as_view(), name="create_update_indi"),
    re_path(r'^(?P<froze_uuid>\w+)/for_print$', dogovor_main_view, name='view'),
]
