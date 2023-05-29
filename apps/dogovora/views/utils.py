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


@csrf_protect
def work_performed(request, froze_uuid):
    """Функционал, для получения списка выполняемых работ, для договоров по сборке мебели."""
    froze = get_object_or_404(Froze, uuid=froze_uuid)
    try:
        dogovor = DogovorIndi.objects.get(froze_id=froze)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('dogovora:create_update', kwargs={'froze_uuid': froze_uuid}))

    work_performed = {}
    for key in (x for x in range(1, 2)):
        work_performed[key] = {}
        work_performed[key]['work_performed_list'] = request.POST.get('work_performed_list_'+str(key)) if request.POST.get('work_performed_list_'+str(key)) else None

    if request.method == "POST" and froze.status != 'pay':
        the_json = dumps(work_performed)
        dogovor.work_performed_list = the_json
        dogovor.save()
    else:
        try:
            the_dict = loads(dogovor.work_performed_list)
            for key in (x for x in range(1, 2)):
                work_performed[key] = the_dict[str(key)]
        except ValueError:
            pass

    return render(request, 'dogovora/list_of_work_in_progress/list_of_work_in_progress.html',
                  {'froze_uuid': froze_uuid, 'froze': froze, 'work_performed': work_performed, 'work_performed_list': True, 'dogovor': dogovor})


@csrf_protect
def montage_demontage(request, froze_uuid):
    """Функционал, для заполнения списка работ по договора монтажа/демонтажа."""
    froze = get_object_or_404(Froze, uuid=froze_uuid)
    try:
        dogovor = DogovorIndi.objects.get(froze_id=froze)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('dogovora:create_update', kwargs={'froze_uuid': froze_uuid}))

    uslugi_installation = {}

    itogo_summa = {}
    itogo_summa['itogo_summa'] = 0

    for key in (x for x in range(1, 11)):
        uslugi_installation[key] = {}
        uslugi_installation[key]['usluga'] = request.POST.get('usluga_'+str(key)) if request.POST.get('usluga_'+str(key)) else None
        uslugi_installation[key]['deadline'] = request.POST.get('deadline_' + str(key)) if request.POST.get('deadline_' + str(key)) else None
        uslugi_installation[key]['tsena'] = request.POST.get('tsena_'+str(key)) if request.POST.get('tsena_'+str(key)) else None

        itogo_summa[key] = uslugi_installation[key]
        try:
            itogo_summa['itogo_summa'] += int(itogo_summa[key]['tsena'])
        except TypeError:
            continue

    if request.method == "POST" and froze.status != 'pay':
        the_json = dumps(uslugi_installation)
        dogovor.list_of_work_installation = the_json
        dogovor.vsego_k_oplate = itogo_summa['itogo_summa']
        dogovor.save()
    else:
        try:
            the_dict = loads(dogovor.list_of_work_installation)
            for key in (x for x in range(1, 11)):
                uslugi_installation[key] = the_dict[str(key)]
        except ValueError:
            pass

    return render(request, 'dogovora/list_of_work_in_progress/list_of_work_installation.html',
                  {'froze_uuid': froze_uuid, 'froze': froze, 'uslugi_installation': uslugi_installation, 'uslugi_montage_demontage': True, 'dogovor': dogovor})


@csrf_protect
def uslugi_po_podklyucheniyu(request, froze_uuid):
    """Функционал, для получения списка выполняемых работ, для услугам подключения"""
    froze = get_object_or_404(Froze, uuid=froze_uuid)
    try:
        dogovor = DogovorIndi.objects.get(froze_id=froze)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('dogovora:create_update', kwargs={'froze_uuid': froze_uuid}))

    uslugi = {}
    for key in (x for x in range(1, 11)):
        uslugi[key] = {}
        uslugi[key]['usluga'] = request.POST.get('usluga_'+str(key)) if request.POST.get('usluga_'+str(key)) else None
        uslugi[key]['tsena'] = request.POST.get('tsena_'+str(key)) if request.POST.get('tsena_'+str(key)) else None

    if request.method == "POST" and froze.status != 'pay':
        the_json = dumps(uslugi)
        dogovor.uslugi_po_podklyucheniyu_tehniki = the_json
        dogovor.save()
    else:
        try:
            the_dict = loads(dogovor.uslugi_po_podklyucheniyu_tehniki)
            for key in (x for x in range(1, 11)):
                uslugi[key] = the_dict[str(key)]
        except ValueError:
            pass

    return render(request, 'dogovora/uslugi_po_podklyucheniyu_create_update.html',
                  {'froze_uuid': froze_uuid, 'froze': froze, 'uslugi': uslugi, 'uslugi_po_podklyucheniyu': True, 'dogovor': dogovor})