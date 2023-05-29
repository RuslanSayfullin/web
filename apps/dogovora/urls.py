from django.urls import path, re_path

from apps.dogovora.views.create_dogovor import nomer_dogovora, drugoy_dogovor, CreateUpdateDogovorIndi
from apps.dogovora.views.print_dogovor import dogovor_main_view
from apps.dogovora.views.utils import teh_usloviya_na_mebel_dveri, tovarnyy_chek

app_name = 'dogovora'
urlpatterns = [
    re_path(r'^nomer_dogovora$', nomer_dogovora, name="nomer_dogovora"),
    re_path(r'^drugoy_dogovor$', drugoy_dogovor, name="drugoy_dogovor"),
    re_path(r'^(?P<froze_uuid>\w+)$', CreateUpdateDogovorIndi.as_view(), name="create_update_indi"),
    re_path(r'^(?P<froze_uuid>\w+)/for_print$', dogovor_main_view, name='view'),
    # Вспомогательные утилиты для при печати договоров
    re_path(r'^(?P<froze_uuid>\w+)/teh_usloviya_na_mebel_dveri/$', teh_usloviya_na_mebel_dveri, name='teh_usloviya_na_mebel_dveri'),
    re_path(r'^(?P<froze_uuid>\w+)/tovarnyy_chek$', tovarnyy_chek, name="tovarnyy_chek"),
]
