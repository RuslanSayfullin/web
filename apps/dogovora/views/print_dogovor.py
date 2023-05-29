from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from apps.dogovora.models import DogovorIndi
from apps.dogovora.views import summa_propisyu
from apps.froze.models import Froze
from json import loads, dumps


def dogovor_main_view(request, froze_uuid):
    froze = get_object_or_404(Froze, uuid=froze_uuid)
    try:
        dogovor = DogovorIndi.objects.get(froze_id=froze)
        if dogovor.nomer_dogovora:
            dogovor.nomer_dogovora = dogovor.nomer_dogovora[1:] if dogovor.nomer_dogovora[0] == '.' else dogovor.nomer_dogovora
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('dogovora:create_update', kwargs={'froze_uuid': froze_uuid}))

    if dogovor.kakoy_tip_dogovora() not in (
        'izgotovlenie_2021_02_mebeli',
        'mygkaya_2021_02_mebel',
        'technic_2021_04',
        'dveri', 'izgotovlenie_mebeli', 'mygkaya_mebel', 'tehnika', 'delivery',
        'izgotovlenie_2019_11_mebeli', 'izgotovlenie_2020_09_mebeli',
        'mygkaya_2019_11_mebel', 'mygkaya_2020_09_mebel',
        'tekstil_ip_sadykov_fiz', 'tekstil_ip_usmanov_fiz',
        'montazh_demontazh_ip_sadykov_fiz',
        'iskusstvenny_kamen', 'iskusstvenny_2021_02_kamen',
        'ekspress_dizayn',
        'podklyuchenie_2021_06_tehniki',
        'matrasy_2021_06',
        'carpets_and_rugs_ip',
        'decoration',
        'gotovaya_mebel_2021_06',
        'kuhonny_2021_07_garnitur_lite',
        'furniture_making',
        'upholstered_furniture',
        'mattresses_ooo-refabrik',
        'carpets_and_rugs_ooo-refabrik',
        'finishedfur_ooo-refabrik',
        'artificial_stone',
        'door_manufacturing',
        'transportation_services',
        'm_furniture_making',
        'm_upholstered_furniture',
        'm_mattresses',
        'm_householdtec',
        'm_connectiontec',
        'm_finishedfur',
        'm_doors',
        'm_stone',
        'm_textile',
        'm_transport',
        'm_assembling',
        'msk_textile_ip_sadykov',
        'msk_textile_ip_usmanov',
        'm_manufacturingassembling',
        'm_furnitureassemblywork',
        'm_2furnitureassemblywork',
        'entity_furniture_making',
        'juridical_moscow_ooo-refabrik_furniture_making',
        'entity_householdtec',
        'juridical_moscow_ooo-refabrik_householdtec',
        'entity_connectiontec',
        'entity_mattresses',
        'juridical_ooo-refabrik_mattresses',
        'entity_finishedfur',
        'juridical_ooo-refabrik_finishedfur',
        'entity_stone',
        'juridical_ooo-refabrik_stone',
        'entity_textile',
        'juridical_moscow_ooo-refabrik_textile',
        'entity_transport',
        'entity_assembling',
        'entity_furnitureassemblywork',
        'juridical_moscow_ooo-refabrik_furnitureassemblywork',
        'entity_ufa_furniture_making',
        'entity_ufa_ooo-refabrik_furniture_making',
        'entity_ufa_householdtec',
        'entity_ufa_ooo-refabrik_householdtec',
        'entity_ufa_connectiontec',
        'entity_ufa_mattresses',
        'entity_ufa_ooo-refabrik_mattresses',
        'entity_ufa_carpets_and_rugs',
        'entity_ufa_finishedfur',
        'entity_ufa_ooo-refabrik_finishedfur',
        'entity_ufa_stone',
        'entity_ufa_ooo-refabrik_stone',
        'entity_ufa_textile',
        'entity_ufa_ooo-refabrik_textile',
        'entity_ufa_transport',
        'entity_ufa_assembling',
    ):
        return HttpResponse('Нужно выбрать другой тип договора! Для данного типа договора, печать недоступна!')
    template = 'dogovora/indi/dogovor_' + dogovor.kakoy_tip_dogovora() + '.html'

    months_v_rod_padezhe = ("", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря")
    RUB_forms = (u'рубль', u'рубля', u'рублей')
    rabochiy_den_forms = (u'рабочий день', u'рабочих дня', u'рабочих дней')
    rabochiy_den_forms_TEHNIKA = (u'рабочего дня', u'рабочих дней', u'рабочих дней')

    dogovor_more = {}
    dogovor_more['data_podpisaniya_month'] = months_v_rod_padezhe[dogovor.data_podpisaniya.month] if dogovor.data_podpisaniya else None

    dogovor_more['nachalo_rabot_data_month'] = months_v_rod_padezhe[dogovor.nachalo_rabot_data.month] if dogovor.nachalo_rabot_data else None
    dogovor_more['okonchanie_rabot_data_month'] = months_v_rod_padezhe[dogovor.okonchanie_rabot_data.month] if dogovor.okonchanie_rabot_data else None

    if dogovor.passport_familiya and dogovor.passport_imya and dogovor.passport_otchestvo:
        dogovor_more['inicialy'] = dogovor.passport_familiya + ' ' + dogovor.passport_imya[0] + '. ' + dogovor.passport_otchestvo[0] + '.'
    if dogovor.oplata_predoplata_rub and dogovor.vsego_k_oplate:
        try:
            dogovor_more['oplata_predoplata_procent'] = round(dogovor.oplata_predoplata_rub / (dogovor.vsego_k_oplate / 100))
        except ZeroDivisionError:
            dogovor_more['oplata_predoplata_procent'] = 0
        dogovor_more['oplata_predoplata_rub'] = '{:,}'.format(dogovor.oplata_predoplata_rub).replace(',', ' ')
        dogovor_more['oplata_predoplata_rub_propisyu'] = summa_propisyu.num2text(dogovor.oplata_predoplata_rub)
        dogovor_more['oplata_predoplata_rub_the_word'] = summa_propisyu.num_words_forms(dogovor.oplata_predoplata_rub, RUB_forms)
        try:
            dogovor_more['nds_oplata_predoplata_rub'] = round(dogovor.oplata_predoplata_rub*20/120, 2)
            dogovor_more['nds_oplata_predoplata_kop'] = (str(dogovor_more['nds_oplata_predoplata_rub'])).split('.')[1]

        except ZeroDivisionError:
            dogovor_more['nds_oplata_predoplata_rub'] = 0
        dogovor_more['nds_oplata_predoplata_rub_propisyu'] = summa_propisyu.num2text(dogovor_more['nds_oplata_predoplata_rub'])
        dogovor_more['nds_oplata_predoplata_rub_the_word'] = summa_propisyu.num_words_forms(dogovor_more['nds_oplata_predoplata_rub'], RUB_forms)

        dogovor_more['oplata_ostatok_procent'] = round(100 - dogovor_more['oplata_predoplata_procent'])
        dogovor_more['oplata_ostatok_rub'] = '{:,}'.format(dogovor.vsego_k_oplate - dogovor.oplata_predoplata_rub).replace(',', ' ')
        dogovor_more['oplata_ostatok_rub_propisyu'] = summa_propisyu.num2text(dogovor.vsego_k_oplate - dogovor.oplata_predoplata_rub)
        dogovor_more['oplata_ostatok_rub_the_word'] = summa_propisyu.num_words_forms(dogovor.vsego_k_oplate - dogovor.oplata_predoplata_rub, RUB_forms)
    if dogovor.vsego_k_oplate:
        dogovor_more['vsego_k_oplate'] = '{:,}'.format(dogovor.vsego_k_oplate).replace(',', ' ')
        dogovor_more['vsego_k_oplate_propisyu'] = summa_propisyu.num2text(dogovor.vsego_k_oplate)
        dogovor_more['vsego_k_oplate_the_word'] = summa_propisyu.num_words_forms(dogovor.vsego_k_oplate, RUB_forms)
        try:
            dogovor_more['nds_k_oplate'] = round(dogovor.vsego_k_oplate*20/120, 2)
            dogovor_more['nds_k_oplate_kop'] = (str(dogovor_more['nds_k_oplate'])).split('.')[1]
        except ZeroDivisionError:
            dogovor_more['nds_k_oplate'] = 0
        dogovor_more['nds_k_oplate_propisyu'] = summa_propisyu.num2text(dogovor_more['nds_k_oplate'])
        dogovor_more['nds_k_oplate_the_word'] = summa_propisyu.num_words_forms(dogovor_more['nds_k_oplate'], RUB_forms)
    if dogovor.summa_za_soputstv_uslugi:
        dogovor_more['summa_za_soputstv_uslugi'] = '{:,}'.format(dogovor.summa_za_soputstv_uslugi).replace(',', ' ')
        dogovor_more['summa_za_soputstv_uslugi_propisyu'] = summa_propisyu.num2text(dogovor.summa_za_soputstv_uslugi)
        dogovor_more['summa_za_soputstv_uslugi_the_word'] = summa_propisyu.num_words_forms(dogovor.summa_za_soputstv_uslugi, RUB_forms)
        try:
            dogovor_more['nds_za_soputstv_uslugi'] = round(dogovor.summa_za_soputstv_uslugi*20/120, 2)
            dogovor_more['nds_za_soputstv_uslugi_kop'] = (str(dogovor_more['nds_za_soputstv_uslugi'])).split('.')[1]
        except ZeroDivisionError:
            dogovor_more['nds_za_soputstv_uslugi'] = 0
        dogovor_more['nds_za_soputstv_uslugi_propisyu'] = summa_propisyu.num2text(dogovor_more['nds_za_soputstv_uslugi'])
        dogovor_more['nds_za_soputstv_uslugi_word'] = summa_propisyu.num_words_forms(dogovor_more['nds_za_soputstv_uslugi'], RUB_forms)
    if dogovor.stoimost_dostavki_vne_ufa:
        dogovor_more['stoimost_dostavki_vne_ufa'] = '{:,}'.format(dogovor.stoimost_dostavki_vne_ufa).replace(',', ' ')
        dogovor_more['stoimost_dostavki_vne_ufa_propisyu'] = summa_propisyu.num2text(dogovor.stoimost_dostavki_vne_ufa)
        dogovor_more['stoimost_dostavki_vne_ufa_the_word'] = summa_propisyu.num_words_forms(dogovor.stoimost_dostavki_vne_ufa, RUB_forms)
        try:
            dogovor_more['nds_za_stoimost_dostavki'] = round(dogovor.stoimost_dostavki_vne_ufa*20/120, 2)
            dogovor_more['nds_za_stoimost_dostavki_kop'] = (str(dogovor_more['nds_za_stoimost_dostavki'])).split('.')[1]
        except ZeroDivisionError:
            dogovor_more['nds_za_stoimost_dostavki'] = 0
        dogovor_more['nds_za_stoimost_dostavki_propisyu'] = summa_propisyu.num2text(dogovor_more['nds_za_stoimost_dostavki'])
        dogovor_more['nds_za_stoimost_dostavki_word'] = summa_propisyu.num_words_forms(dogovor_more['nds_za_stoimost_dostavki'], RUB_forms)
    if dogovor.stoimost_dostavki_vne_ufa == 0:  # FIXME: make not hard code
        dogovor_more['stoimost_dostavki_vne_ufa'] = 0
        dogovor_more['stoimost_dostavki_vne_ufa_propisyu'] = u'ноль'
        dogovor_more['stoimost_dostavki_vne_ufa_the_word'] = u'рублей'

    # Товарный чек - техника
    tovarnyy_chek = None
    if dogovor.kakoy_tip_dogovora() in ('tehnika', 'technic_2021_04', 'matrasy_2021_06', 'carpets_and_rugs_ip',
                                        'carpets_and_rugs_ooo-refabrik',
                                        'decoration', 'gotovaya_mebel_2021_06', 'finishedfur_ooo-refabrik',
                                        'mattresses_ooo-refabrik', 'm_mattresses',
                                        'm_householdtec', 'm_finishedfur', 'entity_householdtec',
                                        'juridical_moscow_ooo-refabrik_householdtec',
                                        'entity_mattresses', 'juridical_ooo-refabrik_mattresses',
                                        'entity_finishedfur', 'juridical_ooo-refabrik_finishedfur',
                                        'entity_ufa_householdtec', 'entity_ufa_ooo-refabrik_householdtec',
                                        'entity_ufa_mattresses', 'entity_ufa_ooo-refabrik_mattresses',
                                        'entity_ufa_carpets_and_rugs',
                                        'entity_ufa_finishedfur', 'entity_ufa_ooo-refabrik_finishedfur'):
        sravn = '{"1": {"tovchek_naim_tovara": null, "tovchek_brand": null, "tovchek_artikul": null, "tovchek_kolvo":' \
                ' null, "tovchek_tsena": null}, "2": {"tovchek_naim_tovara": null, "tovchek_brand": null, "tovchek_ar' \
                'tikul": null, "tovchek_kolvo": null, "tovchek_tsena": null}, "3": {"tovchek_naim_tovara": null, "tov' \
                'chek_brand": null, "tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsena": null}, "4": {"to' \
                'vchek_naim_tovara": null, "tovchek_brand": null, "tovchek_artikul": null, "tovchek_kolvo": null, "to' \
                'vchek_tsena": null}, "5": {"tovchek_naim_tovara": null, "tovchek_brand": null, "tovchek_artikul": nu' \
                'll, "tovchek_kolvo": null, "tovchek_tsena": null}, "6": {"tovchek_naim_tovara": null, "tovchek_brand' \
                '": null, "tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsena": null}, "7": {"tovchek_naim' \
                '_tovara": null, "tovchek_brand": null, "tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsen' \
                'a": null}, "8": {"tovchek_naim_tovara": null, "tovchek_brand": null, "tovchek_artikul": null, "tovch' \
                'ek_kolvo": null, "tovchek_tsena": null}, "9": {"tovchek_naim_tovara": null, "tovchek_brand": null, "' \
                'tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsena": null}, "10": {"tovchek_naim_tovara":' \
                ' null, "tovchek_brand": null, "tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsena": null},'\
                ' "11": {"tovchek_naim_tovara": null, "tovchek_brand": null, "tovchek_artikul": null, "tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsena": null}, ' \
                '"12": {"tovchek_naim_tovara": null, "tovchek_brand": null, "tovchek_artikul": null, "tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsena": null}, ' \
                '"13": {"tovchek_naim_tovara": null, "tovchek_brand": null, "tovchek_artikul": null, "tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsena": null}, ' \
                '"14": {"tovchek_naim_tovara": null, "tovchek_brand": null, "tovchek_artikul": null, "tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsena": null}, ' \
                '"15": {"tovchek_naim_tovara": null, "tovchek_brand": null, "tovchek_artikul": null, "tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsena": null}, ' \
                '"16": {"tovchek_naim_tovara": null, "tovchek_brand": null, "tovchek_artikul": null, "tovchek_artikul": null, "tovchek_kolvo": null, "tovchek_tsena": null},}'
        if dogovor.tovarny_chek_tehnika and dogovor.tovarny_chek_tehnika != sravn:
            try:
                tovarnyy_chek = {}
                the_dict = loads(dogovor.tovarny_chek_tehnika)
                tovarnyy_chek['itogo_summa'] = 0
                for key in (x for x in range(1, 17)):
                    tovarnyy_chek[key] = the_dict[str(key)]
                    try:
                        tovarnyy_chek[key]['summa'] = int(tovarnyy_chek[key]['tovchek_kolvo']) * int(tovarnyy_chek[key]['tovchek_tsena'])
                        tovarnyy_chek['itogo_summa'] += tovarnyy_chek[key]['summa']
                        tovarnyy_chek[key]['summa'] = str(tovarnyy_chek[key]['summa']) + ' руб.'
                        tovarnyy_chek[key]['tovchek_tsena'] = str(tovarnyy_chek[key]['tovchek_tsena']) + ' руб.'
                    except TypeError:
                        continue
            except ValueError:
                tovarnyy_chek = {'don_t_print': True}
        else:
            tovarnyy_chek = {'don_t_print': True}
        try:
            tovarnyy_chek['itogo_summa_propisyu'] = summa_propisyu.num2text(tovarnyy_chek['itogo_summa'])
        except Exception:
            tovarnyy_chek['itogo_summa_propisyu'] = None
    # Товарный чек - техника

    # Список выполняемых работ, для договоров по сборке мебели
    performed_list = None   # инициализируем пустой список выполеякмых работ
    if dogovor.kakoy_tip_dogovora() in ('m_furnitureassemblywork', 'm_2furnitureassemblywork',
                                        'entity_furnitureassemblywork',
                                        'juridical_moscow_ooo-refabrik_furnitureassemblywork'):
        sravn = '{"1": {"work_performed_list": null}, }'
        if dogovor.work_performed_list and dogovor.work_performed_list != sravn:
            try:
                performed_list = {}
                the_dict = loads(dogovor.work_performed_list)
                for key in (x for x in range(1, 2)):
                    performed_list[key] = the_dict[str(key)]
            except ValueError:
                performed_list = {'don_t_print': True}
        else:
            performed_list = {'don_t_print': True}
    # /Список выполняемых работ, для договорам по сборке мебели

    # Список выполняемых работ, для договоров монтаж/демонтаж
    uslugi_installation = None
    if dogovor.kakoy_tip_dogovora() in ('montazh_demontazh_ip_sadykov_fiz', 'entity_ufa_assembling', 'm_assembling', 'entity_assembling'):
        sravn = '{"1": {"usluga": null, "deadline": null, "tsena": null},' \
                '"2": {"usluga": null, "deadline": null, "tsena": null},' \
                '"3": {"usluga": null, "deadline": null, "tsena": null},' \
                '"4": {"usluga": null, "deadline": null, "tsena": null}, ' \
                '"5": {"usluga": null, "deadline": null, "tsena": null}, ' \
                '"6": {"usluga": null, "deadline": null, "tsena": null}, ' \
                '"7": {"usluga": null, "deadline": null, "tsena": null}, ' \
                '"8": {"usluga": null, "deadline": null, "tsena": null}, ' \
                '"9": {"usluga": null, "deadline": null, "tsena": null},' \
                '"10": {"usluga": null, "deadline": null, "tsena": null}}'

        if dogovor.list_of_work_installation and dogovor.list_of_work_installation != sravn:
            try:
                uslugi_installation = {}
                the_dict = loads(dogovor.list_of_work_installation)
                uslugi_installation['itogo_summa'] = 0
                for key in (x for x in range(1, 11)):
                    uslugi_installation[key] = the_dict[str(key)]
                    try:
                        uslugi_installation['itogo_summa'] += int(uslugi_installation[key]['tsena'])
                        uslugi_installation[key]['tsena'] = str(uslugi_installation[key]['tsena'])  # + ' руб.'
                    except TypeError:
                        continue
            except ValueError:
                uslugi_installation = {'don_t_print': True}
        else:
            uslugi_installation = {'don_t_print': True}
        try:
            uslugi_installation['itogo_summa_propisyu'] = summa_propisyu.num2text(uslugi_installation['itogo_summa'])
        except Exception:
            uslugi_installation['itogo_summa_propisyu'] = None
    # /Список выполняемых работ, для договоров монтаж/демонтаж

    # Товарный чек - услуги по подключению бытовой техники
    uslugi = None
    if dogovor.kakoy_tip_dogovora() in ('podklyuchenie_2021_06_tehniki', 'm_connectiontec', 'entity_connectiontec', 'entity_ufa_connectiontec'):
        sravn = '{"1": {"usluga": null, "tsena": null}, "2": {"usluga": null, "tsena": null}, "3": {"usluga": null, "' \
                'tsena": null}, "4": {"usluga": null, "tsena": null}, "5": {"usluga": null, "tsena": null}, "6": {"us' \
                'luga": null, "tsena": null}, "7": {"usluga": null, "tsena": null}, "8": {"usluga": null, "tsena": nu' \
                'll}, "9": {"usluga": null, "tsena": null}, "10": {"usluga": null, "tsena": null}, "11": {"usluga": n' \
                'ull, "tsena": null}, "12": {"usluga": null, "tsena": null}, "13": {"usluga": null, "tsena": null}, "' \
                '14": {"usluga": null, "tsena": null}, "15": {"usluga": null, "tsena": null}, "16": {"usluga": null, ' \
                '"tsena": null}}'
        if dogovor.uslugi_po_podklyucheniyu_tehniki and dogovor.uslugi_po_podklyucheniyu_tehniki != sravn:
            try:
                uslugi = {}
                the_dict = loads(dogovor.uslugi_po_podklyucheniyu_tehniki)
                uslugi['itogo_summa'] = 0
                for key in (x for x in range(1, 11)):
                    uslugi[key] = the_dict[str(key)]
                    try:
                        uslugi['itogo_summa'] += int(uslugi[key]['tsena'])
                        uslugi[key]['tsena'] = str(uslugi[key]['tsena'])  # + ' руб.'
                    except TypeError:
                        continue
            except ValueError:
                uslugi = {'don_t_print': True}
        else:
            uslugi = {'don_t_print': True}
        try:
            uslugi['itogo_summa_propisyu'] = summa_propisyu.num2text(uslugi['itogo_summa'])
        except Exception:
            uslugi['itogo_summa_propisyu'] = None
    # Товарный чек - услуги по подключению бытовой техники

    if dogovor.srok_ispolneniya_rabot:
        dogovor_more['srok_ispolneniya_rabot'] =  '{:,}'.format(dogovor.srok_ispolneniya_rabot).replace(',', ' ')
        dogovor_more['srok_ispolneniya_rabot_propisyu'] = summa_propisyu.num2text(dogovor.srok_ispolneniya_rabot)
        if dogovor.kakoy_tip_dogovora() == 'tehnika':
            dogovor_more['srok_ispolneniya_rabot_the_word'] = summa_propisyu.num_words_forms(dogovor.srok_ispolneniya_rabot, rabochiy_den_forms_TEHNIKA)
        else:
            dogovor_more['srok_ispolneniya_rabot_the_word'] = summa_propisyu.num_words_forms(dogovor.srok_ispolneniya_rabot, rabochiy_den_forms)

    postavshik = dogovor.postavshik()
    if dogovor.doverennye_lica:
        dogovor_more['doverennye_lica'] = dogovor.doverennye_lica.split(',')
    if dogovor.doverennye_lica_telefony:
        dogovor_more['doverennye_lica_telefony'] = dogovor.doverennye_lica_telefony.split(',')

    if dogovor.kakoy_tip_dogovora() in ('technic_2021_04', 'matrasy_2021_06', 'carpets_and_rugs_ip',
                                        'carpets_and_rugs_ooo-refabrik', 'mattresses_ooo-refabrik', 'm_mattresses',
                                        'm_householdtec', 'entity_householdtec',
                                        'juridical_moscow_ooo-refabrik_householdtec',
                                        'entity_mattresses', 'juridical_ooo-refabrik_mattresses',
                                        'entity_ufa_householdtec',
                                        'entity_ufa_ooo-refabrik_householdtec', 'entity_ufa_mattresses',
                                        'entity_ufa_ooo-refabrik_mattresses', 'entity_ufa_carpets_and_rugs') and dogovor.drugoy_dogovor:
        nomer_drugogo_dogovora = str(dogovor.drugoy_dogovor.nomer_dogovora)[1:] if str(dogovor.drugoy_dogovor.nomer_dogovora)[0] == '.' else str(dogovor.drugoy_dogovor.nomer_dogovora)
        nomer_drugogo_dogovora = nomer_drugogo_dogovora + dogovor.drugoy_dogovor.postavshik()['nomer_dog']
        dogovor_more['drugoy_dogovor_nomer'] = nomer_drugogo_dogovora
        dogovor_more['drugoy_dogovor_data_podpisaniya'] = dogovor.drugoy_dogovor.data_podpisaniya
        dogovor_more['drugoy_dogovor_data_podpisaniya_month'] = months_v_rod_padezhe[dogovor.drugoy_dogovor.data_podpisaniya.month] if dogovor.drugoy_dogovor.data_podpisaniya else None

    if dogovor.kakoy_tip_dogovora() == 'kuhonny_2021_07_garnitur_lite':
        template = 'dogovora/dogovor_izgotovlenie_2021_02_mebeli.html'

    return render(request, template, {
        'dogovor': dogovor,
        'froze': froze,
        'dogovor_more': dogovor_more,
        'postavshik': postavshik,
        'tovarnyy_chek': tovarnyy_chek,
        'uslugi': uslugi,
        'performed_list': performed_list,
        'uslugi_installation': uslugi_installation,
    })