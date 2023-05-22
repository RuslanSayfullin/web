from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.formats import date_format

from apps.dogovora.type_of_contracts.types_indi import TIPY_DOGOVOROV
from apps.froze.models import Froze


class DogovorIndi(models.Model):
    """Модель для договоров с физ. лицами"""

    froze = models.OneToOneField(Froze, db_index=True, on_delete=models.CASCADE, verbose_name="Заявка")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    published = models.DateTimeField(default=timezone.now, verbose_name="Дата Создания")

    passport_familiya = models.CharField(max_length=200, default='', db_index=True, blank=True)
    passport_imya = models.CharField(max_length=200, default='', db_index=True, blank=True)
    passport_otchestvo = models.CharField(max_length=200, default='', db_index=True, blank=True)

    passport_birthday_date = models.DateField(default=None, blank=True, null=True)
    passport_birthday_place = models.CharField(max_length=200, default='', blank=True, null=True)
    passport_seria = models.CharField(max_length=4, default=None, blank=True, null=True)
    passport_nomer = models.CharField(max_length=6, default=None, blank=True, null=True)
    passport_kem_vydan = models.CharField(max_length=200, default='', blank=True, null=True)
    passport_kogda_vydan = models.DateField(default=None, blank=True, null=True)
    passport_kp = models.CharField(max_length=7, default=None, blank=True, null=True)
    adres_propiski = models.CharField(max_length=200, default='', blank=True, null=True)
    adres_ustanovki = models.CharField(max_length=200, default='', blank=True, null=True)

    vsego_k_oplate = models.PositiveIntegerField(default=None, blank=True, null=True)
    oplata_predoplata_rub = models.PositiveIntegerField(default=None, blank=True, null=True)
    installment_plan = models.PositiveIntegerField(default=None, blank=True, null=True)                 # Срок рассрочки.
    naimenov_soputstv_izdeliy = models.CharField(max_length=200, default='', blank=True, null=True)     # Наименования сопутствующих изделий
    summa_za_soputstv_uslugi = models.PositiveIntegerField(default=None, blank=True, null=True)         # Указать сумму за сопутств.услугу(если они есть)
    stoimost_dostavki_vne_ufa = models.PositiveIntegerField(default=None, blank=True, null=True)

    data_podpisaniya = models.DateField(default=None, blank=True, null=True)
    srok_ispolneniya_rabot = models.PositiveSmallIntegerField(default=None, blank=True, null=True)
    tip_dogovora = models.CharField(db_index=True, max_length=100, choices=TIPY_DOGOVOROV, default=0, blank=True, null=True, verbose_name="Тип договора")
    nomer_dogovora = models.CharField(max_length=20, default='', blank=True, null=True, verbose_name="Номер договора")  # Номер договора
    tip_opisanie_izdeliya = models.CharField(max_length=500, default='', blank=True, null=True)         # Тип (описание) изделия
    doverennye_lica = models.CharField(max_length=500, default='', blank=True, null=True)               # Доверенные лица
    doverennye_lica_telefony = models.CharField(max_length=500, default='', blank=True, null=True)      # Телефоны доверенных лиц
    nachalo_rabot_data = models.DateField(default=None, blank=True, null=True)                          # Начало работ
    okonchanie_rabot_data = models.DateField(default=None, blank=True, null=True)

    tovarny_chek_tehnika = models.TextField(default='', blank=True, null=True)                          # ТОВАРНЫЙ ЧЕК (10 строк в табл.)
    uslugi_po_podklyucheniyu_tehniki = models.TextField(default='', blank=True, null=True)              # УСЛУГИ ПО ПОДКЛЮЧЕНИЮ БЫТОВОЙ ТЕХНИКИ
    work_performed_list = models.TextField(default='', blank=True, null=True)                           # СПИСОК ВЫПОЛНЯЕМЫХ РАБОТ
    list_of_work_installation = models.TextField(default='', blank=True, null=True)                     # СПИСОК ВЫПОЛНЯЕМЫХ РАБОТ ДЛЯ ДОГОВОРОВ МОНТАЖА
    mygkaya_mebel_prilozhenie = models.TextField(default='', blank=True, null=True)                     # Приложение к договору №1 - mygkaya_mebel

    technics_sroki_dostavki_tehniki = models.PositiveIntegerField(default=None, blank=True, null=True)
    technics_sroki_dostavki_tehniki_v_dnyah = models.PositiveIntegerField(default=None, blank=True, null=True)

    drugoy_dogovor = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "dogovora"
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def get_firstlast_name(self):
        """
        Return the surname_name.
        """
        return self.passport_imya + ' ' + self.passport_familiya

    @property
    def passport_birthday_date_for_bitrix(self):
        passport_birthday_date_for_bitrix = date_format(self.passport_birthday_date, format="d.m.Y") if self.passport_birthday_date else ''
        return passport_birthday_date_for_bitrix

    def __str__(self):
        return '№ {nomer_dogovora} ("{kakoy_tip_dogovora_na_kirillice}", {data_podpisaniya}, {passport_familiya}, ' \
               '{passport_imya1}. {passport_otchestvo1}.)'.format(
                nomer_dogovora=str(self.nomer_dogovora) if self.nomer_dogovora else '',
                kakoy_tip_dogovora_na_kirillice=self.kakoy_tip_dogovora_na_kirillice(),
                data_podpisaniya=date_format(self.data_podpisaniya, format="d.m.Y") if self.data_podpisaniya else '',
                passport_familiya=str(self.passport_familiya) if self.passport_familiya else '',
                passport_imya1=str(self.passport_imya)[:1] if self.passport_imya else '',
                passport_otchestvo1=str(self.passport_otchestvo)[:1] if self.passport_otchestvo else '',
                )

    def kakoy_tip_dogovora(self):
        if self.tip_dogovora is None:
            return ''
        if 'izgotovlenie_2023_06_mebeli' in self.tip_dogovora:
            return 'izgotovlenie_2023_06_mebeli'

    def kakoy_tip_dogovora_na_kirillice(self):
        if self.tip_dogovora is None:
            return ''
        if 'izgotovlenie' in self.tip_dogovora:
            return 'на изготовление мебели'

    def kakoe_yur_lico_na_kirillice(self):
        if 'frolov' in self.tip_dogovora:
            return 'ИП Фролов'
        elif 'bagautdinov' in self.tip_dogovora:
            return 'ИП Багаутдинов'
        elif 'sadykov' in self.tip_dogovora:
            return 'ИП Садыков'
        elif 'hafizov' in self.tip_dogovora:
            return 'ИП Хафизов'

    def postavshik(self):
        postavshik = {}
        postavshik['otkaz'] = {}
        if 'frolov' in self.tip_dogovora:
            postavshik['fio'] = 'Фролов Алексей Александрович'
            postavshik['svidetelstvo'] = ''
            postavshik['adres1'] = '450006, Республика Башкортостан, '
            postavshik['adres2'] = 'г. Уфа, ул. Пархоменко, д.117, кв.37'
            postavshik['adres1_post'] = '450106, Республика Башкортостан, '
            postavshik['adres2_post'] = 'г. Уфа, ул. Менделеева,  д.128, корп.1'
            postavshik['inn'] = '025803156617'
            postavshik['ogrnip'] = '321028000092443'
            postavshik['rs'] = '40802810406000067854'
            postavshik['otkaz']['mygkaya_mebel'] = ''
            postavshik['otkaz']['izgotovlenie_mebeli'] = ''
            postavshik['otkaz']['dveri'] = ''
            postavshik['doverennost'] = 'б/н от 21.06.2021 г.'
            postavshik['adres_poryadok_razresheniya_sporov'] = '__'
        elif 'bagautdinov' in self.tip_dogovora:
            postavshik['fio'] = 'Багаутдинов Эмиль Разитович'
            postavshik['svidetelstvo'] = '007758247 от 23.12.2016'
            postavshik['adres1'] = '452410, Республика Башкортостан,  '
            postavshik['adres2'] = 'г. Уфа, ул. Орджоникидзе, д.19/2, кв. 271'
            postavshik['adres1_post'] = '450112, Республика Башкортостан, '
            postavshik['adres2_post'] = 'г.Уфа, ул.Ульяновых, д. 57'
            postavshik['inn'] = '027319282852'
            postavshik['ogrnip'] = '319028000164001'
            postavshik['rs'] = '40802810606000041421'
            postavshik['otkaz']['mygkaya_mebel'] = '450096, РБ, г. Уфа, ул.Энтузиастов 14'
            postavshik['otkaz']['izgotovlenie_mebeli'] = '450096, РБ, г. Уфа, ул.Энтузиастов 14'
            postavshik['otkaz']['dveri'] = '450096, РБ, г. Уфа, ул.Энтузиастов 14'
            postavshik['doverennost'] = '02 АА 5056584 от 15.11.2019г.'
            postavshik[
                'adres_poryadok_razresheniya_sporov'] = '450096, Республика Башкортостан, г. Уфа, ул. Энтузиастов 14'
        elif 'sadykov' in self.tip_dogovora:
            postavshik['fio'] = 'Садыков Фархад Идиятуллович'
            postavshik['svidetelstvo'] = '007108676 от 03.06.2014'
            postavshik['adres1'] = '452163, Республика Башкортостан, Чишминский р-н,'
            postavshik['adres2'] = 'Новотроицкое с., Школьная ул., дом № 2, кв. 1'
            postavshik['adres1_post'] = '450112, Республика Башкортостан, '
            postavshik['adres2_post'] = 'г. Уфа, ул. Ульяновых, д.57'
            postavshik['inn'] = '022402661350'
            postavshik['ogrnip'] = '314028000072800'
            postavshik['rs'] = '40802810806000015299'
            postavshik['otkaz']['mygkaya_mebel'] = '450112, РБ, г. Уфа, ул. Ульяновых, д. 57'
            postavshik['otkaz']['izgotovlenie_mebeli'] = '450112, РБ, г. Уфа, ул. Ульяновых, д. 57'
            postavshik['otkaz']['dveri'] = '450112, Республика Башкортостан,  г. Уфа, ул. Ульяновых, д. 57'
            postavshik['doverennost'] = '02 АА 4175422  от 15.02.2018г.'
            if self.tip_dogovora == 'tekstil_ip_sadykov_fiz':
                postavshik['doverennost'] = '02 АА 5116982  от 03.09.2020 г.'  # Текстиль
            postavshik[
                'adres_poryadok_razresheniya_sporov'] = '450112, Республика Башкортостан, г. Уфа, ул. Ульяновых, д. 57'
        elif 'hafizov' in self.tip_dogovora:
            postavshik['fio'] = 'Хафизов Азат Ильдарович'
            postavshik['svidetelstvo'] = '007857653 от 23.12.2016'
            postavshik['adres1'] = '450017, Республика Башкортостан, г.Уфа,'
            postavshik['adres2'] = 'ул. Ахметова, дом № 320, корп. 1, кв. 122'
            postavshik['adres1_post'] = '450022, Республика Башкортостан, '
            postavshik['adres2_post'] = 'г.Уфа, ул.Менделеева, д.145'
            postavshik['inn'] = '027813125266'
            postavshik['ogrnip'] = '316028000223382'
            postavshik['rs'] = '40802810406000015589'
            postavshik['otkaz']['mygkaya_mebel'] = '450022, РБ, г. Уфа, ул. Менделеева, д. 145'
            postavshik['otkaz']['izgotovlenie_mebeli'] = '450022, РБ, г. Уфа, ул. Менделеева, д. 145'
            postavshik['otkaz']['dveri'] = '450022, РБ, г. Уфа, ул. Менделеева, д. 145'
            postavshik['doverennost'] = '02 АА 5056586 от 15.11.2019г.'
            postavshik[
                'adres_poryadok_razresheniya_sporov'] = '450022, Республика Башкортостан, г. Уфа, ул. Менделеева, д. 145'
        elif 'usmanov' in self.tip_dogovora:
            postavshik['fio'] = 'Усманов Тимур Рамилевич'
            postavshik['svidetelstvo'] = '643115891 от 25.03.2022'
            postavshik['adres1'] = '450017, Республика Башкортостан, г.Уфа,'
            postavshik['adres2'] = 'ул. Рудольфа Нуреева, дом № 1, кв. 232'
            postavshik['adres1_post'] = '450022, Республика Башкортостан, '
            postavshik['adres2_post'] = 'г. Уфа, ул. Ульяновых, д.57'
            postavshik['inn'] = '025501238101'
            postavshik['ogrnip'] = '322028000057043'
            postavshik['rs'] = '40802810106000057339'
            postavshik['otkaz']['mygkaya_mebel'] = '450022, РБ, г. Уфа, ул. Ульяновых, д.57'
            postavshik['otkaz']['izgotovlenie_mebeli'] = '450022, РБ, г. Уфа, ул. Ульяновых, д.57'
            postavshik['otkaz']['dveri'] = '450022, РБ, г. Уфа, ул. Ульяновых, д.57'



