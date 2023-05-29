from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect

from apps.dogovora.models import DogovorIndi
from apps.froze.models import Froze
from django.urls import reverse_lazy, reverse
from json import loads, dumps


def teh_usloviya_na_mebel_dveri(request, froze_uuid):
    """Печать тех. условий, для договоров"""
    froze = get_object_or_404(Froze, uuid=froze_uuid)
    try:
        dogovor = DogovorIndi.objects.get(froze_id=froze)
        dogovor_more = {}
        months_v_rod_padezhe = ("", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря")
        dogovor_more['data_podpisaniya_month'] = months_v_rod_padezhe[dogovor.data_podpisaniya.month] if dogovor.data_podpisaniya else None
        if dogovor.passport_familiya and dogovor.passport_imya and dogovor.passport_otchestvo:
            dogovor_more['inicialy'] = dogovor.passport_familiya + ' ' + dogovor.passport_imya[0] + '. ' + dogovor.passport_otchestvo[0] + '.'
        context = {
            'dogovor': dogovor,
            'dogovor_more': dogovor_more,
        }
        return render(request, 'dogovora/teh_usloviya_na_mebel_dveri.html', context)
    except DogovorIndi.DoesNotExist:
        return render(request, 'dogovora/teh_usloviya_na_mebel_dveri.html', None)


@csrf_protect
def tovarnyy_chek(request, froze_uuid):
    """Функционал, для заполнения товарного чека. Данные из данного чека, буду распечатаны в основном договоре"""
    froze = get_object_or_404(Froze, uuid=froze_uuid)
    try:
        dogovor = DogovorIndi.objects.get(froze_id=froze)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('dogovora:create_update', kwargs={'froze_uuid': froze_uuid}))

    ten_1_10 = {}
    itogo_summa = {}
    itogo_summa['itogo_summa'] = 0

    for key in (x for x in range(1, 17)):
        ten_1_10[key] = {}
        ten_1_10[key]['tovchek_naim_tovara'] = request.POST.get('tovchek_naim_tovara_'+str(key)) if request.POST.get('tovchek_naim_tovara_'+str(key)) else None
        ten_1_10[key]['tovchek_brand'] = request.POST.get('tovchek_brand_'+str(key)) if request.POST.get('tovchek_brand_'+str(key)) else None
        ten_1_10[key]['tovchek_artikul'] = request.POST.get('tovchek_artikul_'+str(key)) if request.POST.get('tovchek_artikul_'+str(key)) else None
        ten_1_10[key]['tovchek_kolvo'] = request.POST.get('tovchek_kolvo_'+str(key)) if request.POST.get('tovchek_kolvo_'+str(key)) else None
        ten_1_10[key]['tovchek_tsena'] = request.POST.get('tovchek_tsena_'+str(key)) if request.POST.get('tovchek_tsena_'+str(key)) else None

        itogo_summa[key] = ten_1_10[key]
        try:
            itogo_summa[key]['summa'] = int(itogo_summa[key]['tovchek_kolvo']) * int(itogo_summa[key]['tovchek_tsena'])
            itogo_summa['itogo_summa'] += itogo_summa[key]['summa']
        except TypeError:
            continue

    if request.method == "POST" and froze.status != 'pay':
        the_json = dumps(ten_1_10)
        dogovor.tovarny_chek_tehnika = the_json
        dogovor.vsego_k_oplate = itogo_summa['itogo_summa']
        dogovor.save()
    else:
        try:
            the_dict = loads(dogovor.tovarny_chek_tehnika)
            for key in (x for x in range(1, 17)):
                ten_1_10[key] = the_dict[str(key)]
        except ValueError:
            pass

    return render(request, 'dogovora/tovarnyy_chek_tehnika_create_update.html',
                  {'froze_uuid': froze_uuid, 'froze': froze, 'ten_1_10': ten_1_10, 'tovarnyy_chek': True, })