import datetime, calendar
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from apps.dogovora.models import DogovorIndi
from apps.dogovora.views import summa_propisyu
from apps.froze.models import Froze


def add_months_installment(sourcedate, months):
    """Используется для расчёта графика платежей по внутренней рассрочке"""
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


@csrf_protect
def supplementary_agreement(request, froze_uuid):
    """Функционал для доп.соглашений пл внутренней рассрочке"""
    froze = get_object_or_404(Froze, uuid=froze_uuid)
    try:
        dogovor = DogovorIndi.objects.get(froze_id=froze)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('dogovora:create_update', kwargs={'froze_uuid': froze_uuid}))

    installment = dogovor.installment_plan  # срок рассрочки
    installment_sum = dogovor.vsego_k_oplate - dogovor.oplata_predoplata_rub    # сумма рассрочки
    mounthly_sum = installment_sum // installment                               # ежемесячный платёж
    last_sum = installment_sum % installment                                    # остаток
    postavshik = dogovor.postavshik()       # юр. лицо, на которого оформлена рассрочка
    dogovor_more = {}
    months_v_rod_padezhe = (" ", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря")  # для корректного представления даты
    RUB_forms = (u'рубль', u'рубля', u'рублей')     # для корректного представления валюты
    # даты платежа
    data_platejya_pervyi = add_months_installment(dogovor.data_podpisaniya, 1)
    data_platejya_vtoroy = add_months_installment(dogovor.data_podpisaniya, 2)
    data_platejya_tretii = add_months_installment(dogovor.data_podpisaniya, 3)
    data_platejya_chetvertyi = add_months_installment(dogovor.data_podpisaniya, 4)
    data_platejya_pyatii = add_months_installment(dogovor.data_podpisaniya, 5)
    data_platejya_chestoy = add_months_installment(dogovor.data_podpisaniya, 6)


    # инициализируем пустой словарь, для шаблона
    dogovor_more['data_podpisaniya_month'] = months_v_rod_padezhe[dogovor.data_podpisaniya.month] if dogovor.data_podpisaniya else None
    if dogovor.vsego_k_oplate:
        dogovor_more['vsego_k_oplate'] = '{:,}'.format(dogovor.vsego_k_oplate).replace(',', ' ')
        dogovor_more['vsego_k_oplate_propisyu'] = summa_propisyu.num2text(dogovor.vsego_k_oplate)
        dogovor_more['vsego_k_oplate_the_word'] = summa_propisyu.num_words_forms(dogovor.vsego_k_oplate, RUB_forms)
    if dogovor.oplata_predoplata_rub and dogovor.vsego_k_oplate:
        try:
            dogovor_more['oplata_predoplata_procent'] = round(dogovor.oplata_predoplata_rub / (dogovor.vsego_k_oplate / 100))
        except ZeroDivisionError:
            dogovor_more['oplata_predoplata_procent'] = 0
        dogovor_more['oplata_predoplata_rub'] = '{:,}'.format(dogovor.oplata_predoplata_rub).replace(',', ' ')
        dogovor_more['oplata_predoplata_rub_propisyu'] = summa_propisyu.num2text(dogovor.oplata_predoplata_rub)
        dogovor_more['oplata_predoplata_rub_the_word'] = summa_propisyu.num_words_forms(dogovor.oplata_predoplata_rub, RUB_forms)
        dogovor_more['oplata_ostatok_procent'] = round(100 - dogovor_more['oplata_predoplata_procent'])
        dogovor_more['oplata_ostatok_rub'] = '{:,}'.format(dogovor.vsego_k_oplate - dogovor.oplata_predoplata_rub).replace(',', ' ')
        dogovor_more['oplata_ostatok_rub_propisyu'] = summa_propisyu.num2text(dogovor.vsego_k_oplate - dogovor.oplata_predoplata_rub)
        dogovor_more['oplata_ostatok_rub_the_word'] = summa_propisyu.num_words_forms(dogovor.vsego_k_oplate - dogovor.oplata_predoplata_rub, RUB_forms)
    if dogovor.installment_plan:    # срок рассрочки
        dogovor_more['installment_plan'] = '{:,}'.format(dogovor.installment_plan).replace(',', ' ')
        dogovor_more['installment_plan'] = summa_propisyu.num2text(dogovor.installment_plan)
        dogovor_more['installment_plan'] = summa_propisyu.num_words_forms(dogovor.installment_plan, RUB_forms)
    if 7 > installment > 0:
        for key in (x for x in range(1, installment+1)):
            dogovor_more[key] = {}
            dogovor_more['mounthly_sum'] = mounthly_sum
            dogovor_more['last_sum'] = last_sum
            if dogovor.passport_familiya and dogovor.passport_imya and dogovor.passport_otchestvo:
                dogovor_more['inicialy'] = dogovor.passport_familiya + ' ' + dogovor.passport_imya[0] + '. ' + dogovor.passport_otchestvo[0] + '.'
            if installment == 1:
                dogovor_more['data_platejya_pervyi'] = data_platejya_pervyi
                dogovor_more['data_platejya_pervyi_month'] = months_v_rod_padezhe[data_platejya_pervyi.month] if data_platejya_pervyi else None
                dogovor_more['platej_pervyi_sum'] = (dogovor_more['mounthly_sum']+dogovor_more['last_sum'])
                dogovor_more['platej_pervyi_rub_propisyu'] = summa_propisyu.num2text(dogovor_more['platej_pervyi_sum'])
            if installment == 2:
                dogovor_more['data_platejya_vtoroy'] = data_platejya_vtoroy
                dogovor_more['data_platejya_vtoroy_month'] = months_v_rod_padezhe[data_platejya_vtoroy.month] if data_platejya_vtoroy else None
                dogovor_more['platej_vtoroy_sum'] = dogovor_more['mounthly_sum']
                dogovor_more['platej_vtoroy_rub_propisyu'] = summa_propisyu.num2text(dogovor_more['platej_vtoroy_sum'])
            if installment == 3:
                dogovor_more['data_platejya_tretii'] = data_platejya_tretii
                dogovor_more['data_platejya_tretii_month'] = months_v_rod_padezhe[data_platejya_tretii.month] if data_platejya_tretii else None
                dogovor_more['platej_tretii_sum'] = dogovor_more['mounthly_sum']
                dogovor_more['platej_tretii_rub_propisyu'] = summa_propisyu.num2text(dogovor_more['platej_tretii_sum'])
            if installment == 4:
                dogovor_more['data_platejya_chetvertyi'] = data_platejya_chetvertyi
                dogovor_more['data_platejya_chetvertyi_month'] = months_v_rod_padezhe[data_platejya_chetvertyi.month] if data_platejya_chetvertyi else None
                dogovor_more['platej_chetvertyi_sum'] = dogovor_more['mounthly_sum']
                dogovor_more['platej_chetvertyi_rub_propisyu'] = summa_propisyu.num2text(dogovor_more['platej_chetvertyi_sum'])
            if installment == 5:
                dogovor_more['data_platejya_pyatii'] = data_platejya_pyatii
                dogovor_more['data_platejya_pyatii_month'] = months_v_rod_padezhe[data_platejya_pyatii.month] if data_platejya_pyatii else None
                dogovor_more['platej_pyatii_sum'] = dogovor_more['mounthly_sum']
                dogovor_more['platej_pyatii_rub_propisyu'] = summa_propisyu.num2text(dogovor_more['platej_pyatii_sum'])
            if installment == 6:
                dogovor_more['data_platejya_chestoy'] = data_platejya_chestoy
                dogovor_more['data_platejya_chestoy_month'] = months_v_rod_padezhe[data_platejya_chestoy.month] if data_platejya_chestoy else None
                dogovor_more['platej_chestoy_sum'] = dogovor_more['mounthly_sum']
                dogovor_more['platej_chestoy_rub_propisyu'] = summa_propisyu.num2text(dogovor_more['platej_chestoy_sum'])
            installment = installment - 1


    # Выбираем свой шаблон по видам договоров
    if dogovor.kakoy_tip_dogovora() in (
            'm_furniture_making', 'm_upholstered_furniture', 'm_doors', 'm_stone',
            'izgotovlenie_2021_02_mebeli', 'mygkaya_2021_02_mebel', 'dveri', 'iskusstvenny_2021_02_kamen',
    ):
        template = 'dogovora/installment/supplementary_agreement.html'
    elif dogovor.kakoy_tip_dogovora() in (
            'tekstil_ip_sadykov_fiz', 'm_textile', 'msk_textile_ip_sadykov', 'msk_textile_ip_usmanov'
    ):
        template = 'dogovora/installment/supplementary_agreement2.html'
    elif dogovor.kakoy_tip_dogovora() in (
            'gotovaya_mebel_2021_06', 'm_finishedfur'
    ):
        template = 'dogovora/installment/supplementary_agreement3.html'
    elif dogovor.kakoy_tip_dogovora() in (
            'furniture_making', 'upholstered_furniture', 'door_manufacturing', 'artificial_stone'
    ):
        template = 'dogovora/installment/supplementary_agreement4.html'
    elif dogovor.kakoy_tip_dogovora() in (
            'technic_2021_04', 'm_householdtec'
    ):
        template = 'dogovora/installment/supplementary_agreement5.html'

    return render(request, template,
                  {'froze_uuid': froze_uuid,
                   'froze': froze,
                   'dogovor': dogovor,
                   'dogovor_more': dogovor_more,
                   'postavshik': postavshik})
