from django.urls import path, re_path


from apps.dogovora.views.create_dogovor import nomer_dogovora, drugoy_dogovor, CreateUpdateDogovorIndi, \
    CreateUpdateDogovorEntry
from apps.dogovora.views.print_dogovor import dogovor_main_view, dogovor_main_view_entry
from apps.dogovora.views.supplementary_agreement import supplementary_agreement
from apps.dogovora.views.utils import teh_usloviya_na_mebel_dveri, tovarnyy_chek, work_performed, montage_demontage, \
    uslugi_po_podklyucheniyu

app_name = 'dogovora'
urlpatterns = [
    re_path(r'^nomer_dogovora$', nomer_dogovora, name="nomer_dogovora"),
    re_path(r'^drugoy_dogovor$', drugoy_dogovor, name="drugoy_dogovor"),
    re_path(r'^indi/(?P<froze_uuid>\w+)/$', CreateUpdateDogovorIndi.as_view(), name="create_update_indi"),
    re_path(r'^entry/(?P<froze_uuid>\w+)/$', CreateUpdateDogovorEntry.as_view(), name="create_update_entry"),


    re_path(r'^(?P<froze_uuid>\w+)/for_print$', dogovor_main_view, name='view'),                    # расспечатать договор ФЛ
    re_path(r'^(?P<froze_uuid>\w+)/for_entry_print$', dogovor_main_view_entry, name='view_entry'),  # расспечатать договор ЮЛ

    # Вспомогательные утилиты для при печати договоров
    re_path(r'^(?P<froze_uuid>\w+)/teh_usloviya_na_mebel_dveri/$', teh_usloviya_na_mebel_dveri, name='teh_usloviya_na_mebel_dveri'),
    re_path(r'^(?P<froze_uuid>\w+)/tovarnyy_chek$', tovarnyy_chek, name="tovarnyy_chek"),
    re_path(r'^(?P<froze_uuid>\w+)/work_performed$', work_performed, name="work_performed"),
    re_path(r'^(?P<froze_uuid>\w+)/list_of_work_installation$', montage_demontage, name="list_of_work_installation"),       # список работ для договоров монтаж/демонтаж
    re_path(r'^(?P<froze_uuid>\w+)/uslugi_po_podklyucheniyu$', uslugi_po_podklyucheniyu, name="uslugi_po_podklyucheniyu"),
    re_path(r'^(?P<froze_uuid>\w+)/teh_usloviya_na_mebel_dveri/$', teh_usloviya_na_mebel_dveri, name='teh_usloviya_na_mebel_dveri'),
    re_path(r'^(?P<froze_uuid>\w+)/supplementary_agreement$', supplementary_agreement, name="supplementary_agreement"),
]
