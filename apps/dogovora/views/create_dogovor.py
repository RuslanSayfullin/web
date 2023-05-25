from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect

from apps.dogovora import forms
from apps.dogovora.models import DogovorIndi
from apps.froze.models import Froze


def novy_nomer_dogovora_():
    try:
        novy_nomer_dogovora = DogovorIndi.objects.filter(nomer_dogovora__istartswith='.').order_by('-published').exclude(nomer_dogovora=None).exclude(nomer_dogovora='')[0].nomer_dogovora
        novy_nomer_dogovora = int(novy_nomer_dogovora[1:5]) + 1
        if novy_nomer_dogovora <= 999:
            novy_nomer_dogovora = '.0' + str(novy_nomer_dogovora)
        else:
            novy_nomer_dogovora = '.' + str(novy_nomer_dogovora)
    except Exception:
        novy_nomer_dogovora = '.0001'
    return novy_nomer_dogovora


@csrf_protect
def nomer_dogovora(request):
    if request.method != 'POST':
        raise PermissionDenied
    self_id = int(request.POST.get('self_id'))
    dogovor = DogovorIndi.objects.get(id=self_id)
    if dogovor.froze.status == 'pay':
        raise PermissionDenied
    if not request.POST.get('id_from_existing_dogovor'):
        dogovor.nomer_dogovora = novy_nomer_dogovora_()
        dogovor.published = timezone.now()
        dogovor.save()
    else:
        id_from_existing_dogovor = int(request.POST.get('id_from_existing_dogovor'))
        dogovor_s_nomerom = DogovorIndi.objects.get(id=id_from_existing_dogovor)
        if dogovor_s_nomerom.nomer_dogovora[0] == '.':
            dogovor.nomer_dogovora = dogovor_s_nomerom.nomer_dogovora[1:]
        else:
            dogovor.nomer_dogovora = dogovor_s_nomerom.nomer_dogovora
        dogovor.save()
    nomer_dogovora = dogovor.nomer_dogovora[1:] if dogovor.nomer_dogovora[0] == '.' else dogovor.nomer_dogovora
    return HttpResponse(nomer_dogovora)


@csrf_protect
def drugoy_dogovor(request):
    if request.method != 'POST' or not request.POST.get('id_dogovora_na_izgotovlenie_mebeli'):
        raise PermissionDenied
    self_id = int(request.POST.get('self_id'))
    id_dogovora_na_izgotovlenie_mebeli = int(request.POST.get('id_dogovora_na_izgotovlenie_mebeli'))
    dogovor = get_object_or_404(DogovorIndi, id=self_id)
    if dogovor.froze.status == 'pay':
        raise PermissionDenied

    dogovor_na_izgotovlenie_mebeli = get_object_or_404(DogovorIndi, id=id_dogovora_na_izgotovlenie_mebeli)
    dogovor.drugoy_dogovor = dogovor_na_izgotovlenie_mebeli
    dogovor.save()
    return HttpResponse(str(dogovor_na_izgotovlenie_mebeli))


def nomer_dogovora_for_tekstil():
    nomera = DogovorIndi.objects.filter(tip_dogovora__in=('tekstil_ip_sadykov_fiz', 'tekstil_ip_usmanov_fiz', 'msk_textile_ip_sadykov', 'msk_textile_ip_usmanov'))\
        .exclude(nomer_dogovora='').values_list('nomer_dogovora', flat=True)
    if nomera:
        try:
            nomera_int = [int(x) for x in nomera]
            return max(nomera_int) + 1
        except (ValueError, IndexError):
            pass
    return '1'


class CreateUpdateDogovorIndi(generic.FormView):
    template_name = 'dogovora/create_update_indi.html'
    form_class = forms.DogovorIndiForm
    froze = None
    froze_uuid = None
    dogovor = None
    create_or_update = None

    def get_context_data(self, **kwargs):
        context = super(CreateUpdateDogovorIndi, self).get_context_data(**kwargs)

        if self.create_or_update == 'update' and (self.dogovor.nomer_dogovora is None or self.dogovor.nomer_dogovora == ''):
            try:
                dogovora_s_takimi_zhe_fio = DogovorIndi.objects.filter(
                    passport_familiya=self.dogovor.passport_familiya,
                    passport_imya=self.dogovor.passport_imya,
                    passport_otchestvo=self.dogovor.passport_otchestvo) \
                    .exclude(passport_familiya='', passport_imya='', passport_otchestvo='') \
                    .exclude(tip_dogovora__in=('tekstil_ip_sadykov_fiz',
                                               'tekstil_ip_usmanov_fiz',
                                               'm_textile',
                                               'msk_textile_ip_sadykov',
                                               'msk_textile_ip_usmanov',
                                               'entity_textile',
                                               'juridical_moscow_ooo-refabrik_textile',
                                               'entity_ufa_textile',
                                               'entity_ufa_ooo-refabrik_textile')) \
                    .exclude(id=self.dogovor.id).exclude(nomer_dogovora=None).exclude(nomer_dogovora='').count()
                drugie_dogovora = DogovorIndi.objects.filter(
                    passport_familiya=self.dogovor.passport_familiya,
                    passport_imya=self.dogovor.passport_imya,
                    passport_otchestvo=self.dogovor.passport_otchestvo) \
                    .exclude(passport_familiya='', passport_imya='', passport_otchestvo='') \
                    .exclude(id=self.dogovor.id).exclude(nomer_dogovora=None).exclude(nomer_dogovora='')
                for dd in drugie_dogovora:
                    dd.nomer_dogovora = dd.nomer_dogovora[1:] if dd.nomer_dogovora[0] == '.' else dd.nomer_dogovora
            except AttributeError:
                dogovora_s_takimi_zhe_fio = 0
                drugie_dogovora = None

            novy_nomer_dogovora = novy_nomer_dogovora_()[1:]
        else:
            dogovora_s_takimi_zhe_fio = None
            drugie_dogovora = None
            novy_nomer_dogovora = None

        """Если это техника, матрасы или ковровые покрытия, то привязываем к договорам по мягкой мебели или корпусной мебели"""
        if self.create_or_update == 'update' and self.dogovor.tip_dogovora is not None and \
                self.dogovor.kakoy_tip_dogovora() in ('technic_2021_04',
                                                      'matrasy_2021_06',
                                                      'carpets_and_rugs_ip',
                                                      'carpets_and_rugs_ooo-refabrik',
                                                      'mattresses_ooo-refabrik',
                                                      'm_mattresses',
                                                      'm_householdtec',
                                                      'entity_householdtec',
                                                      'juridical_moscow_ooo-refabrik_householdtec',
                                                      'entity_mattresses',
                                                      'juridical_ooo-refabrik_mattresses',
                                                      'entity_ufa_householdtec',
                                                      'entity_ufa_ooo-refabrik_householdtec',
                                                      'entity_ufa_mattresses',
                                                      'entity_ufa_ooo-refabrik_mattresses',
                                                      'entity_ufa_carpets_and_rugs'):
            dogovora_na_izgotovlenie_mebeli = DogovorIndi.objects.filter(
                passport_familiya=self.dogovor.passport_familiya,
                passport_imya=self.dogovor.passport_imya,
                passport_otchestvo=self.dogovor.passport_otchestvo).filter(Q(tip_dogovora__contains='izgotovlenie_')    # выборка договора на изготовление мебели, к которым можно привязать договоры на технику и матрасы
                                                                           | Q(tip_dogovora__contains='mygkaya_')
                                                                           | Q(tip_dogovora__contains='furniture_making_')
                                                                           | Q(tip_dogovora__contains='upholstered_furniture_')
                                                                           | Q(tip_dogovora__contains='m_furniture_')
                                                                           | Q(tip_dogovora__contains='m_upholstered_')
                                                                           | Q(tip_dogovora__contains='m_manufacturingassembling_')
                                                                           | Q(tip_dogovora__contains='entity_furniture_making')
                                                                           | Q(tip_dogovora__contains='juridical_moscow_ooo-refabrik_furniture_making')
                                                                           | Q(tip_dogovora__contains='entity_ufa_furniture_making')
                                                                           | Q(tip_dogovora__contains='entity_ufa_ooo-refabrik_furniture_making')
                                                                           | Q(tip_dogovora__contains='iskusstvenny_2021_02_kamen')
                                                                           | Q(tip_dogovora__contains='artificial_stone')
                                                                           | Q(tip_dogovora__contains='entity_ufa_stone')
                                                                           | Q(tip_dogovora__contains='entity_ufa_ooo-refabrik_stone')
                                                                           | Q(tip_dogovora__contains='m_stone')
                                                                           | Q(tip_dogovora__contains='entity_stone')
                                                                           | Q(tip_dogovora__contains='juridical_ooo-refabrik_stone')
                                                                           )\
                .exclude(passport_familiya='', passport_imya='', passport_otchestvo='') \
                .exclude(id=self.dogovor.id).exclude(nomer_dogovora=None).exclude(nomer_dogovora='')
        else:
            dogovora_na_izgotovlenie_mebeli = None

        context.update({
            'froze_uuid': self.kwargs.get('froze_uuid'),
            'froze': self.froze,
            'create_or_update': self.create_or_update,
            'dogovor': self.dogovor,

            'dogovora_s_takimi_zhe_fio': dogovora_s_takimi_zhe_fio,
            'drugie_dogovora': drugie_dogovora,
            'novy_nomer_dogovora': novy_nomer_dogovora,
            'dogovora_na_izgotovlenie_mebeli': dogovora_na_izgotovlenie_mebeli,
            'self_id': self.dogovor.id or None,
        })
        return context

    def dispatch(self, *args, **kwargs):
        self.froze_uuid = kwargs.get('froze_uuid')
        self.froze = get_object_or_404(Froze, uuid=self.froze_uuid)
        try:
            self.dogovor = DogovorIndi.objects.get(froze_id=self.froze)
            self.create_or_update = 'update'
        except ObjectDoesNotExist:
            self.create_or_update = 'create'
        return super(CreateUpdateDogovorIndi, self).dispatch(*args, **kwargs)

    def get_initial(self):
        if self.create_or_update == 'update':
            passport_birthday_date = str(self.dogovor.passport_birthday_date.strftime("%d.%m.%Y")) if self.dogovor.passport_birthday_date else self.dogovor.passport_birthday_date
            passport_kogda_vydan = str(self.dogovor.passport_kogda_vydan.strftime("%d.%m.%Y")) if self.dogovor.passport_kogda_vydan else self.dogovor.passport_kogda_vydan
            data_podpisaniya = str(self.dogovor.data_podpisaniya.strftime("%d.%m.%Y")) if self.dogovor.data_podpisaniya else None
            nachalo_rabot_data = str(self.dogovor.nachalo_rabot_data.strftime("%d.%m.%Y")) if self.dogovor.nachalo_rabot_data else None
            okonchanie_rabot_data = str(self.dogovor.okonchanie_rabot_data.strftime("%d.%m.%Y")) if self.dogovor.okonchanie_rabot_data else None
            if self.dogovor.nomer_dogovora:
                nomer_dogovora = self.dogovor.nomer_dogovora[1:] if self.dogovor.nomer_dogovora[0] == '.' else self.dogovor.nomer_dogovora
            else:
                nomer_dogovora = None

            initial = {
                'passport_familiya': self.dogovor.passport_familiya,
                'passport_imya': self.dogovor.passport_imya,
                'passport_otchestvo': self.dogovor.passport_otchestvo,

                'passport_birthday_date': passport_birthday_date,
                'passport_birthday_place': self.dogovor.passport_birthday_place,
                'passport_seria': self.dogovor.passport_seria,
                'passport_nomer': self.dogovor.passport_nomer,
                'passport_kem_vydan': self.dogovor.passport_kem_vydan,
                'passport_kogda_vydan': passport_kogda_vydan,
                'passport_kp': self.dogovor.passport_kp,
                'adres_propiski': self.dogovor.adres_propiski if self.dogovor.adres_propiski else None,
                'adres_ustanovki': self.dogovor.adres_ustanovki if self.dogovor.adres_ustanovki else None,
                'vsego_k_oplate': self.dogovor.vsego_k_oplate if self.dogovor.vsego_k_oplate or self.dogovor.vsego_k_oplate == 0 else None,
                'oplata_predoplata_rub': self.dogovor.oplata_predoplata_rub if self.dogovor.oplata_predoplata_rub or self.dogovor.oplata_predoplata_rub == 0 else None,
                'naimenov_soputstv_izdeliy': self.dogovor.naimenov_soputstv_izdeliy if self.dogovor.naimenov_soputstv_izdeliy else None,
                'summa_za_soputstv_uslugi': self.dogovor.summa_za_soputstv_uslugi if self.dogovor.summa_za_soputstv_uslugi or self.dogovor.summa_za_soputstv_uslugi == 0 else None,
                'stoimost_dostavki_vne_ufa': self.dogovor.stoimost_dostavki_vne_ufa if self.dogovor.stoimost_dostavki_vne_ufa or self.dogovor.stoimost_dostavki_vne_ufa == 0 else None,
                'data_podpisaniya': data_podpisaniya,
                'srok_ispolneniya_rabot': self.dogovor.srok_ispolneniya_rabot if self.dogovor.srok_ispolneniya_rabot or self.dogovor.srok_ispolneniya_rabot == 0 else None,
                'installment_plan': self.dogovor.installment_plan if self.dogovor.installment_plan or self.dogovor.installment_plan == 0 else None,
                'tip_dogovora': self.dogovor.tip_dogovora if self.dogovor.tip_dogovora else None,

                'nomer_dogovora': nomer_dogovora,
                'drugoy_dogovor': self.dogovor.drugoy_dogovor if self.dogovor.drugoy_dogovor else None,
                'tip_opisanie_izdeliya': self.dogovor.tip_opisanie_izdeliya if self.dogovor.tip_opisanie_izdeliya else None,
                'doverennye_lica': self.dogovor.doverennye_lica if self.dogovor.doverennye_lica else None,
                'doverennye_lica_telefony': self.dogovor.doverennye_lica_telefony if self.dogovor.doverennye_lica_telefony else None,
                'nachalo_rabot_data': nachalo_rabot_data,
                'okonchanie_rabot_data': okonchanie_rabot_data,
                'sposob_oplaty': self.froze.type_pay,

                'technics_sroki_dostavki_tehniki': self.dogovor.technics_sroki_dostavki_tehniki if self.dogovor.technics_sroki_dostavki_tehniki else None,
                'technics_sroki_dostavki_tehniki_v_dnyah': self.dogovor.technics_sroki_dostavki_tehniki_v_dnyah if self.dogovor.technics_sroki_dostavki_tehniki_v_dnyah else None,
            }
            return initial.copy()
        elif self.create_or_update == 'create':
            return super(CreateUpdateDogovorIndi, self).get_initial()

    def form_valid(self, form):
        if self.froze.status == 'pay':
            return super(CreateUpdateDogovorIndi, self).form_invalid(form)

        if form.cleaned_data.get('sposob_oplaty'):
            self.froze.type_pay = form.cleaned_data.get('sposob_oplaty')
            self.froze.save(update_fields=('type_pay',))
        if form.cleaned_data.get('tip_opisanie_izdeliya'):
            self.froze.type_production = form.cleaned_data.get('tip_opisanie_izdeliya')
            self.froze.save(update_fields=('type_production',))


        passport_familiya = form.cleaned_data.get('passport_familiya')
        passport_imya = form.cleaned_data.get('passport_imya')
        passport_otchestvo = form.cleaned_data.get('passport_otchestvo')

        passport_birthday_date = form.cleaned_data.get('passport_birthday_date')
        passport_birthday_place = form.cleaned_data.get('passport_birthday_place')
        passport_seria = form.cleaned_data.get('passport_seria')
        passport_nomer = form.cleaned_data.get('passport_nomer')
        passport_kem_vydan = form.cleaned_data.get('passport_kem_vydan')
        passport_kogda_vydan = form.cleaned_data.get('passport_kogda_vydan')
        passport_kp = form.cleaned_data.get('passport_kp')
        adres_propiski = form.cleaned_data.get('adres_propiski') if form.cleaned_data.get('adres_propiski') else None
        adres_ustanovki = form.cleaned_data.get('adres_ustanovki') if form.cleaned_data.get('adres_ustanovki') else None

        vsego_k_oplate = form.cleaned_data.get('vsego_k_oplate') if form.cleaned_data.get('vsego_k_oplate') or form.cleaned_data.get('vsego_k_oplate') == 0 else None
        oplata_predoplata_rub = form.cleaned_data.get('oplata_predoplata_rub') if form.cleaned_data.get('oplata_predoplata_rub') or form.cleaned_data.get('oplata_predoplata_rub') == 0 else None
        naimenov_soputstv_izdeliy = form.cleaned_data.get('naimenov_soputstv_izdeliy') if form.cleaned_data.get('naimenov_soputstv_izdeliy') else None
        summa_za_soputstv_uslugi = form.cleaned_data.get('summa_za_soputstv_uslugi') if form.cleaned_data.get('summa_za_soputstv_uslugi') or form.cleaned_data.get('summa_za_soputstv_uslugi') == 0 else None
        stoimost_dostavki_vne_ufa = form.cleaned_data.get('stoimost_dostavki_vne_ufa') if form.cleaned_data.get('stoimost_dostavki_vne_ufa') or form.cleaned_data.get('stoimost_dostavki_vne_ufa') == 0 else None
        data_podpisaniya = form.cleaned_data.get('data_podpisaniya')
        srok_ispolneniya_rabot = form.cleaned_data.get('srok_ispolneniya_rabot') if form.cleaned_data.get('srok_ispolneniya_rabot') or form.cleaned_data.get('srok_ispolneniya_rabot') == 0 else None
        installment_plan = form.cleaned_data.get('installment_plan') if form.cleaned_data.get('installment_plan') or form.cleaned_data.get('installment_plan') == 0 else None
        tip_dogovora = form.cleaned_data.get('tip_dogovora') if form.cleaned_data.get('tip_dogovora') else None

        nomer_dogovora = form.cleaned_data.get('nomer_dogovora') if form.cleaned_data.get('nomer_dogovora') else None
        tip_opisanie_izdeliya = form.cleaned_data.get('tip_opisanie_izdeliya') if form.cleaned_data.get('tip_opisanie_izdeliya') else None
        doverennye_lica = form.cleaned_data.get('doverennye_lica') if form.cleaned_data.get('doverennye_lica') else None
        doverennye_lica_telefony = form.cleaned_data.get('doverennye_lica_telefony') if form.cleaned_data.get('doverennye_lica_telefony') else None
        nachalo_rabot_data = form.cleaned_data.get('nachalo_rabot_data') if form.cleaned_data.get('nachalo_rabot_data') else None
        okonchanie_rabot_data = form.cleaned_data.get('okonchanie_rabot_data') if form.cleaned_data.get('okonchanie_rabot_data') else None

        technics_sroki_dostavki_tehniki = form.cleaned_data.get('technics_sroki_dostavki_tehniki') if form.cleaned_data.get('technics_sroki_dostavki_tehniki') else None
        technics_sroki_dostavki_tehniki_v_dnyah = form.cleaned_data.get('technics_sroki_dostavki_tehniki_v_dnyah') if form.cleaned_data.get('technics_sroki_dostavki_tehniki_v_dnyah') else None

        if self.create_or_update == 'update':
            self.dogovor.passport_familiya = passport_familiya
            self.dogovor.passport_imya = passport_imya
            self.dogovor.passport_otchestvo = passport_otchestvo

            self.dogovor.passport_birthday_date = passport_birthday_date
            self.dogovor.passport_birthday_place = passport_birthday_place
            self.dogovor.passport_seria = passport_seria
            self.dogovor.passport_nomer = passport_nomer
            self.dogovor.passport_kem_vydan = passport_kem_vydan
            self.dogovor.passport_kogda_vydan = passport_kogda_vydan
            self.dogovor.passport_kp = passport_kp
            self.dogovor.adres_propiski = adres_propiski if adres_propiski else None
            self.dogovor.adres_ustanovki = adres_ustanovki if adres_ustanovki else None
            self.dogovor.vsego_k_oplate = vsego_k_oplate if vsego_k_oplate or vsego_k_oplate == 0 else None
            self.dogovor.oplata_predoplata_rub = oplata_predoplata_rub if oplata_predoplata_rub or oplata_predoplata_rub == 0 else None
            self.dogovor.naimenov_soputstv_izdeliy = naimenov_soputstv_izdeliy if naimenov_soputstv_izdeliy else None
            self.dogovor.summa_za_soputstv_uslugi = summa_za_soputstv_uslugi if summa_za_soputstv_uslugi or summa_za_soputstv_uslugi == 0 else None
            self.dogovor.stoimost_dostavki_vne_ufa = stoimost_dostavki_vne_ufa if stoimost_dostavki_vne_ufa or stoimost_dostavki_vne_ufa == 0 else None
            self.dogovor.data_podpisaniya = data_podpisaniya if data_podpisaniya else None
            self.dogovor.srok_ispolneniya_rabot = srok_ispolneniya_rabot if srok_ispolneniya_rabot or srok_ispolneniya_rabot == 0 else None
            self.dogovor.installment_plan = installment_plan if installment_plan or installment_plan == 0 else None
            self.dogovor.tip_dogovora = tip_dogovora
            if not self.dogovor.nomer_dogovora and (tip_dogovora == 'tekstil_ip_sadykov_fiz' or tip_dogovora == 'tekstil_ip_usmanov_fiz' or tip_dogovora == 'msk_textile_ip_sadykov' or tip_dogovora == 'msk_textile_ip_usmanov'):
                self.dogovor.nomer_dogovora = nomer_dogovora_for_tekstil()
            elif nomer_dogovora:
                self.dogovor.nomer_dogovora = nomer_dogovora
            self.dogovor.tip_opisanie_izdeliya = tip_opisanie_izdeliya if tip_opisanie_izdeliya else None
            self.dogovor.doverennye_lica = doverennye_lica if doverennye_lica else None
            self.dogovor.doverennye_lica_telefony = doverennye_lica_telefony if doverennye_lica_telefony else None
            self.dogovor.nachalo_rabot_data = nachalo_rabot_data if nachalo_rabot_data else None
            self.dogovor.okonchanie_rabot_data = okonchanie_rabot_data if okonchanie_rabot_data else None

            self.dogovor.technics_sroki_dostavki_tehniki = technics_sroki_dostavki_tehniki if technics_sroki_dostavki_tehniki else None
            self.dogovor.technics_sroki_dostavki_tehniki_v_dnyah = technics_sroki_dostavki_tehniki_v_dnyah if technics_sroki_dostavki_tehniki_v_dnyah else None

            self.dogovor.save()
            return super(CreateUpdateDogovorIndi, self).form_valid(form)
        elif self.create_or_update == 'create':
            author = self.request.user
            with transaction.atomic():
                DogovorIndi.objects.create(
                    froze=self.froze,
                    author=author,

                    passport_familiya=passport_familiya,
                    passport_imya=passport_imya,
                    passport_otchestvo=passport_otchestvo,

                    passport_birthday_date=passport_birthday_date,
                    passport_birthday_place=passport_birthday_place,
                    passport_seria=passport_seria,
                    passport_nomer=passport_nomer,
                    passport_kem_vydan=passport_kem_vydan,
                    passport_kogda_vydan=passport_kogda_vydan,
                    passport_kp=passport_kp,
                    adres_propiski=adres_propiski,
                    adres_ustanovki=adres_ustanovki,
                    vsego_k_oplate=vsego_k_oplate,
                    oplata_predoplata_rub=oplata_predoplata_rub,
                    naimenov_soputstv_izdeliy=naimenov_soputstv_izdeliy,
                    summa_za_soputstv_uslugi=summa_za_soputstv_uslugi,
                    stoimost_dostavki_vne_ufa=stoimost_dostavki_vne_ufa,
                    data_podpisaniya=data_podpisaniya,
                    srok_ispolneniya_rabot=srok_ispolneniya_rabot,
                    installment_plan=installment_plan,
                    tip_dogovora=tip_dogovora,
                    tip_opisanie_izdeliya=tip_opisanie_izdeliya,
                    doverennye_lica=doverennye_lica,
                    doverennye_lica_telefony=doverennye_lica_telefony,
                    nachalo_rabot_data=nachalo_rabot_data,
                    okonchanie_rabot_data=okonchanie_rabot_data,
                    technics_sroki_dostavki_tehniki=technics_sroki_dostavki_tehniki,
                    technics_sroki_dostavki_tehniki_v_dnyah=technics_sroki_dostavki_tehniki_v_dnyah,
                )
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('dogovora:create_update_indi', args=(self.kwargs.get('froze_uuid'),))
