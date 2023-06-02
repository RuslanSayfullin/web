from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.formats import date_format

from apps.dogovora.type_of_contracts.types_entry import TIPY_DOGOVOROV_ENTRY
from apps.dogovora.type_of_contracts.types_indi import TIPY_DOGOVOROV
from apps.froze.models import Froze


class DogovorIndi(models.Model):
    """Модель для договоров с физ. лицами"""

    TIPY_DOGOVOROV = TIPY_DOGOVOROV

    froze = models.OneToOneField(Froze, db_index=True, on_delete=models.CASCADE, verbose_name="Заявка")
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
        if 'izgotovlenie_2021_02_mebeli' in self.tip_dogovora:
            return 'izgotovlenie_2021_02_mebeli'
        if 'mygkaya_2021_02_mebel' in self.tip_dogovora:
            return 'mygkaya_2021_02_mebel'
        if 'technic_2021_04' in self.tip_dogovora:
            return 'technic_2021_04'
        if 'podklyuchenie_2021_06_tehniki' in self.tip_dogovora:
            return 'podklyuchenie_2021_06_tehniki'
        if 'matrasy_2021_06' in self.tip_dogovora:
            return 'matrasy_2021_06'
        if 'carpets_and_rugs_ip' in self.tip_dogovora:
            return 'carpets_and_rugs_ip'
        if 'decoration' in self.tip_dogovora:
            return 'decoration'
        if 'gotovaya_mebel_2021_06' in self.tip_dogovora:
            return 'gotovaya_mebel_2021_06'
        if 'iskusstvenny_2021_02_kamen' in self.tip_dogovora:
            return 'iskusstvenny_2021_02_kamen'
        if self.tip_dogovora == 'tekstil_ip_sadykov_fiz':
            return 'tekstil_ip_sadykov_fiz'
        if self.tip_dogovora == 'tekstil_ip_usmanov_fiz':
            return 'tekstil_ip_usmanov_fiz'
        if 'dveri' in self.tip_dogovora:
            return 'dveri'
        if 'delivery' in self.tip_dogovora:
            return 'delivery'
        if self.tip_dogovora == 'montazh_demontazh_ip_sadykov_fiz':
            return 'montazh_demontazh_ip_sadykov_fiz'
        if 'ekspress_dizayn' in self.tip_dogovora:
            return 'ekspress_dizayn'

        """Договоры физ.лиц с ООО Ре-фабрик"""
        if 'furniture_making_ooo-refabrik' in self.tip_dogovora:
            return 'furniture_making'
        if 'upholstered_furniture_ooo-refabrik' in self.tip_dogovora:
            return 'upholstered_furniture'
        if self.tip_dogovora == 'mattresses_ooo-refabrik':
            return 'mattresses_ooo-refabrik'
        if self.tip_dogovora == 'carpets_and_rugs_ooo-refabrik':
            return 'carpets_and_rugs_ooo-refabrik'
        if self.tip_dogovora == 'finishedfur_ooo-refabrik':
            return 'finishedfur_ooo-refabrik'
        if 'artificial_stone_ooo-refabrik' in self.tip_dogovora:
            return 'artificial_stone'
        if 'door_manufacturing_ooo-refabrik' in self.tip_dogovora:
            return 'door_manufacturing'
        if 'transportation_services_ooo-refabrik' in self.tip_dogovora:
            return 'transportation_services'

        """Московские договоры с физ. лицами"""
        if 'm_furniture_making' in self.tip_dogovora:
            return 'm_furniture_making'
        if 'm_upholstered_furniture' in self.tip_dogovora:
            return 'm_upholstered_furniture'
        if 'm_mattresses' in self.tip_dogovora:
            return 'm_mattresses'
        if 'm_householdtec' in self.tip_dogovora:
            return 'm_householdtec'
        if 'm_connectiontec' in self.tip_dogovora:
            return 'm_connectiontec'
        if 'm_finishedfur' in self.tip_dogovora:
            return 'm_finishedfur'
        if 'm_doors' in self.tip_dogovora:
            return 'm_doors'
        if 'm_stone' in self.tip_dogovora:
            return 'm_stone'
        if 'm_textile' in self.tip_dogovora:
            return 'm_textile'
        if self.tip_dogovora == 'msk_textile_ip_sadykov':
            return 'msk_textile_ip_sadykov'
        if self.tip_dogovora == 'msk_textile_ip_usmanov':
            return 'msk_textile_ip_usmanov'
        if 'm_transport' in self.tip_dogovora:
            return 'm_transport'
        if 'm_assembling' in self.tip_dogovora:
            return 'm_assembling'
        if 'm_manufacturingassembling' in self.tip_dogovora:
            return 'm_manufacturingassembling'
        if 'm_furnitureassemblywork' in self.tip_dogovora:
            return 'm_furnitureassemblywork'
        if 'm_2furnitureassemblywork' in self.tip_dogovora:
            return 'm_2furnitureassemblywork'

        """ДОГОВОРЫ по подарочным серификатами"""
        if 'gift_certificate' in self.tip_dogovora:
            return 'gift_certificate'


    def kakoy_tip_dogovora_na_kirillice(self):
        if self.tip_dogovora is None:
            return ''
        if 'izgotovlenie' in self.tip_dogovora:
            return 'на изготовление мебели'
        if 'mygkaya' in self.tip_dogovora:
            return 'на мягкую мебель'
        if 'technic_2021_04' in self.tip_dogovora:
            return 'Техника'
        if 'podklyuchenie' in self.tip_dogovora:
            return 'Подключение техники'
        if 'matrasy' in self.tip_dogovora:
            return 'на матрасы'
        if 'carpets_and_rugs_ip' in self.tip_dogovora:
            return 'Ковры и ковровые покрытия'
        if 'decoration' in self.tip_dogovora:
            return 'Декор'
        if 'gotovaya' in self.tip_dogovora:
            return 'мебели выстовочного образца'
        if 'iskusstvenny' in self.tip_dogovora:
            return 'на изготовление изделий из искусственного камня'
        if self.tip_dogovora == 'tekstil_ip_sadykov_fiz':
            return 'на изготовление текстильных изделий и сопутсвующих услуг'
        if self.tip_dogovora == 'tekstil_ip_usmanov_fiz':
            return 'на изготовление текстильных изделий и сопутсвующих услуг'
        if 'dveri' in self.tip_dogovora:
            return 'на двери'
        if 'delivery' in self.tip_dogovora:
            return 'Оказание транспортных услуг'
        if self.tip_dogovora == 'montazh_demontazh_ip_sadykov_fiz':
            return 'Монтаж/демонтаж | ИП Садыков | Физ'
        if 'ekspress_dizayn' in self.tip_dogovora:
            return 'Экспресс дизайн–проект'

        """Договоры физ.лиц с ООО Ре-фабрик"""
        if self.tip_dogovora == 'furniture_making_ooo-refabrik':
            return 'на изготовление мебели'
        if self.tip_dogovora == 'upholstered_furniture_ooo-refabrik':
            return 'Мягкая мебель ООО «Ре-фабрик»'
        if self.tip_dogovora == 'mattresses_ooo-refabrik':
            return 'Матрасы ООО «Ре-фабрик»'
        if self.tip_dogovora == 'carpets_and_rugs_ooo-refabrik':
            return 'Ковры и ковровые покрытия ООО «Ре-фабрик»'
        if self.tip_dogovora == 'finishedfur_ooo-refabrik':
            return 'мебели выстовочного образца ООО «Ре-фабрик»'
        if self.tip_dogovora == 'martificial_stone_ooo-refabrik':
            return 'на изготовление изделий из искусственного камня'
        if self.tip_dogovora == 'door_manufacturing_ooo-refabrik':
            return 'Двери ООО «Ре-фабрик»'
        if self.tip_dogovora == 'transportation_services_ooo-refabrik':
            return 'Оказание транспортных услуг «Ре-фабрик»'

        """Московские договоры с физ. лицами"""
        if 'm_furniture_making' in self.tip_dogovora:
            return 'на изготовление мебели'
        if 'm_upholstered_furniture' in self.tip_dogovora:
            return 'на изготовление мягкой мебели'
        if 'm_mattresses' in self.tip_dogovora:
            return 'М матрасы ФЗ'
        if 'm_householdtec' in self.tip_dogovora:
            return 'М бытовая техника ФЗ'
        if 'm_connectiontec' in self.tip_dogovora:
            return 'М подключение техники ФЗ'
        if 'm_finishedfur' in self.tip_dogovora:
            return 'мебели выстовочного образца'
        if 'm_doors' in self.tip_dogovora:
            return 'на изготовление и поставку межкомнатных дверей, отделку'
        if 'm_stone' in self.tip_dogovora:
            return 'на изготовление изделий из искусственного камня'
        if 'm_textile' in self.tip_dogovora:
            return 'на изготовление текстильных изделий и сопутствующих услуг'
        if self.tip_dogovora == 'msk_textile_ip_sadykov' or self.tip_dogovora == 'msk_textile_ip_usmanov':
            return 'на изготовление текстильных изделий и сопутсвующих услуг'
        if 'm_transport' in self.tip_dogovora:
            return 'М транспортные услуги ФЗ'
        if 'm_assembling' in self.tip_dogovora:
            return 'М Монтаж/демонтаж ФЗ'
        if 'm_manufacturingassembling' in self.tip_dogovora:
            return 'М Изготовление/монтаж мягкой мебели ФЗ'
        if 'm_furnitureassemblywork' in self.tip_dogovora:
            return 'М Выполнение работ по сборке мебели ФЗ'
        if 'm_2furnitureassemblywork' in self.tip_dogovora:
            return 'М (по согласованию) Выполнение работ по сборке мебели ФЗ'

        """ДОГОВОРЫ по подарочным серификатами"""
        if 'gift_certificate' in self.tip_dogovora:
            return 'Подарочные сертификаты'


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

        elif 'ooo-refabrik' in self.tip_dogovora:
            postavshik['fio'] = 'ООО РЕ - ФАБРИК'
            postavshik['svidetelstvo'] = ''
            postavshik['adres1'] = '450022, Республика Башкортостан, '
            postavshik['adres2'] = 'г. Уфа, ул. Менделеева,  д.145, пом.20'
            postavshik['adres1_post'] = '450112, Республика Башкортостан, '
            postavshik['adres2_post'] = 'г. Уфа, ул. Ульяновых, д.57'
            postavshik['inn'] = '0278931524'
            postavshik['kpp'] = '027801001'
            postavshik['ogrn'] = '1170280042008'
            postavshik['rs'] = '40702810306000021744'
            postavshik['otkaz']['izgotovlenie_mebeli'] = ''
            # postavshik['otkaz']['mygkaya_mebel'] = ''
            # postavshik['otkaz']['dveri'] = ''
            postavshik['doverennost'] = '-'
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
        else:
            postavshik['fio'] = '___ ____ ___________'
            postavshik['svidetelstvo'] = ''
            postavshik['adres1'] = '__________________'
            postavshik['adres2'] = '__________________'
            postavshik['adres1_post'] = '__________________'
            postavshik['adres2_post'] = '__________________'
            postavshik['inn'] = '__________________'
            postavshik['ogrnip'] = '__________________'
            postavshik['rs'] = '__________________'
            postavshik['doverennost'] = '__________________'

        postavshik['nomer_dog'] = postavshik['fio'][0]
        postavshik['bank1'] = 'БАШКИРСКОЕ ОТДЕЛЕНИЕ № 8598'
        postavshik['bank2'] = 'ПАО СБЕРБАНК г. УФА'
        postavshik['ks'] = '30101810300000000601'
        postavshik['bik'] = '048073601'
        inicialy = postavshik['fio'].split(' ')
        postavshik['inicialy'] = inicialy[0] + ' ' + inicialy[1][0:1] + '.' + inicialy[2][0:1] + '.'
        return postavshik


class DogovorEntry(models.Model):
    class Meta:
        db_table = "dogovora_entry"
        verbose_name = 'Договор ЮЛ'
        verbose_name_plural = 'Договоры ЮЛ'

    TIPY_DOGOVOROV = TIPY_DOGOVOROV_ENTRY
    froze = models.OneToOneField(Froze, db_index=True, on_delete=models.CASCADE, verbose_name="Заявка")
    published = models.DateTimeField(default=timezone.now, verbose_name="Дата Создания")

    passport_familiya = models.CharField(max_length=200, default='', db_index=True, blank=True)
    passport_imya = models.CharField(max_length=200, default='', db_index=True, blank=True)
    passport_otchestvo = models.CharField(max_length=200, default='', db_index=True, blank=True)

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
    okonchanie_rabot_data = models.DateField(default=None, blank=True, null=True)                       # Окончание работ

    tovarny_chek_tehnika = models.TextField(default='', blank=True, null=True)                          # ТОВАРНЫЙ ЧЕК (10 строк в табл.)
    uslugi_po_podklyucheniyu_tehniki = models.TextField(default='', blank=True, null=True)              # УСЛУГИ ПО ПОДКЛЮЧЕНИЮ БЫТОВОЙ ТЕХНИКИ
    work_performed_list = models.TextField(default='', blank=True, null=True)                           # СПИСОК ВЫПОЛНЯЕМЫХ РАБОТ
    list_of_work_installation = models.TextField(default='', blank=True, null=True)                     # СПИСОК ВЫПОЛНЯЕМЫХ РАБОТ ДЛЯ ДОГОВОРОВ МОНТАЖА
    mygkaya_mebel_prilozhenie = models.TextField(default='', blank=True, null=True)                     # Приложение к договору №1 - mygkaya_mebel

    technics_sroki_dostavki_tehniki = models.PositiveIntegerField(default=None, blank=True, null=True)
    technics_sroki_dostavki_tehniki_v_dnyah = models.PositiveIntegerField(default=None, blank=True, null=True)

    drugoy_dogovor = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    # Поля, необходимые для оформления договоров с юр. лицами.
    general_director = models.CharField(max_length=200, default='', blank=True, null=True)              # ФИО, представителя организаций.
    job_title = models.CharField(max_length=200, default='', blank=True, null=True)                     # должность, представителя организаций.
    letter_of_attorney = models.CharField(max_length=200, default='', blank=True, null=True)            # доверенность, представителя организаций.
    tax_identification_number = models.CharField(max_length=12, default=None, blank=True, null=True)    # ИНН
    registration_reason_code = models.CharField(max_length=9, default='', blank=True, null=True)        # КПП
    registration_number = models.CharField(max_length=15, default=None, blank=True, null=True)          # ОГРН/ОГРНИП
    checking_account = models.CharField(max_length=20, default='', blank=True, null=True)               # расчётный счёт юридического лица
    account_bank = models.CharField(max_length=200, default='', blank=True, null=True)                  # банк
    correspondent_account = models.CharField(max_length=20, default='', blank=True, null=True)          # Корреспондентский счёт юридического лица
    bank_identification_code = models.CharField(max_length=9, default='', blank=True, null=True)        # БИК юридического лица

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
        """Договоры юр.лиц с ООО ФМ «Реформа» Уфа"""
        if 'entity_ufa_furniture_making' in self.tip_dogovora:
            return 'entity_ufa_furniture_making'
        if 'entity_ufa_householdtec_fabrika_mebeli_reforma' in self.tip_dogovora:
            return 'entity_ufa_householdtec'
        if 'entity_ufa_connectiontec' in self.tip_dogovora:
            return 'entity_ufa_connectiontec'
        if 'entity_ufa_mattresses' in self.tip_dogovora:
            return 'entity_ufa_mattresses'
        if self.tip_dogovora == 'entity_ufa_carpets_and_rugs_fabrika_mebeli_reforma':
            return 'entity_ufa_carpets_and_rugs'
        if 'entity_ufa_finishedfur' in self.tip_dogovora:
            return 'entity_ufa_finishedfur'
        if 'entity_ufa_stone' in self.tip_dogovora:
            return 'entity_ufa_stone'
        if 'entity_ufa_textile' in self.tip_dogovora:
            return 'entity_ufa_textile'
        if 'entity_ufa_transport' in self.tip_dogovora:
            return 'entity_ufa_transport'
        if 'entity_ufa_assembling' in self.tip_dogovora:
            return 'entity_ufa_assembling'

        """Договоры юр.лиц с ООО «Ре-фабрик» Уфа"""
        if 'entity_ufa_ooo-refabrik_furniture_makin' in self.tip_dogovora:
            return 'entity_ufa_ooo-refabrik_furniture_making'
        if 'entity_ufa_ooo-refabrik_mattresses' in self.tip_dogovora:
            return 'entity_ufa_ooo-refabrik_mattresses'
        if 'entity_ufa_ooo-refabrik_householdtec' in self.tip_dogovora:
            return 'entity_ufa_ooo-refabrik_householdtec'
        if 'entity_ufa_ooo-refabrik_finishedfur' in self.tip_dogovora:
            return 'entity_ufa_ooo-refabrik_finishedfur'
        if 'entity_ufa_ooo-refabrik_stone' in self.tip_dogovora:
            return 'entity_ufa_ooo-refabrik_stone'
        if 'entity_ufa_ooo-refabrik_textile' in self.tip_dogovora:
            return 'entity_ufa_ooo-refabrik_textile'

        """Договоры юр.лиц с ООО «Ре-форма плюс»"""
        if 'entity_furniture_making' in self.tip_dogovora:
            return 'entity_furniture_making'
        if 'entity_householdtec' in self.tip_dogovora:
            return 'entity_householdtec'
        if 'entity_connectiontec' in self.tip_dogovora:
            return 'entity_connectiontec'
        if 'entity_mattresses' in self.tip_dogovora:
            return 'entity_mattresses'
        if 'entity_finishedfur' in self.tip_dogovora:
            return 'entity_finishedfur'
        if 'entity_stone' in self.tip_dogovora:
            return 'entity_stone'
        if 'entity_textile' in self.tip_dogovora:
            return 'entity_textile'
        if 'entity_transport' in self.tip_dogovora:
            return 'entity_transport'
        if 'entity_assembling' in self.tip_dogovora:
            return 'entity_assembling'
        if 'entity_furnitureassemblywork' in self.tip_dogovora:
            return 'entity_furnitureassemblywork'

        """ДОГОВОРЫ С ЮР. ЛИЦАМИ ООО Фабрика мебели «Реформа»"""
        if self.tip_dogovora == 'juridical_furniture_making_fabrika_mebeli_reforma':
            return 'entity_furniture_making'
        if self.tip_dogovora == 'juridical_householdtec_fabrika_mebeli_reforma':
            return 'entity_householdtec'
        if self.tip_dogovora == 'juridical_connectiontec_fabrika_mebeli_reforma':
            return 'entity_connectiontec'
        if self.tip_dogovora == 'juridical_mattresses_fabrika_mebeli_reforma':
            return 'entity_mattresses'
        if self.tip_dogovora == 'juridical_finishedfur_fabrika_mebeli_reforma':
            return 'entity_finishedfur'
        if self.tip_dogovora == 'juridical_stone_reforma_fabrika_mebeli_reforma':
            return 'entity_stone'
        if self.tip_dogovora == 'juridical_textile_reforma_fabrika_mebeli_reforma':
            return 'entity_textile'
        if self.tip_dogovora == 'juridical_transport_reforma_fabrika_mebeli_reforma':
            return 'entity_transport'
        if self.tip_dogovora == 'juridical_assembling_reforma_fabrika_mebeli_reforma':
            return 'entity_assembling'
        if self.tip_dogovora == 'juridical_furnitureassemblywork_fabrika_mebeli_reforma':
            return 'entity_furnitureassemblywork'

        # ДОГОВОРЫ С ЮР. ЛИЦАМИ ООО «Ре-фабрик» Москва
        if self.tip_dogovora == 'juridical_moscow_ooo-refabrik_furniture_making':
            return 'juridical_moscow_ooo-refabrik_furniture_making'
        if self.tip_dogovora == 'juridical_moscow_ooo-refabrik_householdtec':
            return 'juridical_moscow_ooo-refabrik_householdtec'
        if self.tip_dogovora == 'juridical_ooo-refabrik_mattresses':
            return 'juridical_ooo-refabrik_mattresses'
        if self.tip_dogovora == 'juridical_ooo-refabrik_finishedfur':
            return 'juridical_ooo-refabrik_finishedfur'
        if self.tip_dogovora == 'juridical_ooo-refabrik_stone':
            return 'juridical_ooo-refabrik_stone'
        if self.tip_dogovora == 'juridical_moscow_ooo-refabrik_furnitureassemblywork':
            return 'juridical_moscow_ooo-refabrik_furnitureassemblywork'
        if self.tip_dogovora == 'juridical_moscow_ooo-refabrik_textile':
            return 'juridical_moscow_ooo-refabrik_textile'


    def kakoy_tip_dogovora_na_kirillice(self):
        if self.tip_dogovora is None:
            return ''
        """Договоры юр.лиц с ООО ФМ «Реформа» Уфа"""
        if 'entity_ufa_furniture_making' in self.tip_dogovora:
            return 'на изготовление мебели'
        if 'entity_ufa_householdtec_fabrika_mebeli_reforma' in self.tip_dogovora:
            return 'Уфа, бытовая техника юр. лица'
        if 'entity_ufa_connectiontec' in self.tip_dogovora:
            return 'Уфа, подключение техники юр. лица'
        if 'entity_ufa_mattresses' in self.tip_dogovora:
            return 'Уфа, матрасы юр. лица'
        if self.tip_dogovora == 'entity_ufa_carpets_and_rugs_fabrika_mebeli_reforma':
            return 'Уфа, ковры и ковровые покрытия'
        if 'entity_ufa_finishedfur' in self.tip_dogovora:
            return 'Уфа,  выставочного образца юр. лица'
        if 'entity_ufa_stone' in self.tip_dogovora:
            return 'на изготовление изделий из искусственного камня'
        if 'entity_ufa_textile' in self.tip_dogovora:
            return 'Уфа, на изготовление текстильных изделий и сопутствующих услуг юр. лица'
        if 'entity_ufa_transport' in self.tip_dogovora:
            return 'Уфа, транспортные услуги юр. лица'
        if 'entity_ufa_assembling' in self.tip_dogovora:
            return 'Уфа Монтаж/демонтаж юр. лица'

        """Договоры юр.лиц с ООО «Ре-фабрик» Уфа"""
        if 'entity_ufa_ooo-refabrik_furniture_making' in self.tip_dogovora:
            return 'на изготовление мебели'
        if 'entity_ufa_ooo-refabrik_mattresses' in self.tip_dogovora:
            return 'Уфа, матрасы юр. лица'
        if 'entity_ufa_ooo-refabrik_householdtec' in self.tip_dogovora:
            return 'Уфа, бытовая техника юр. лица'
        if 'entity_ufa_ooo-refabrik_finishedfur' in self.tip_dogovora:
            return 'Уфа, мебель выставочного образца юр. лица'
        if 'entity_ufa_ooo-refabrik_stone' in self.tip_dogovora:
            return 'на изготовление изделий из искусственного камня'
        if 'entity_ufa_ooo-refabrik_textile' in self.tip_dogovora:
            return 'Уфа, на изготовление текстильных изделий и сопутствующих услуг юр. лица'

        """Договоры юр.лиц с ООО «Ре-форма плюс»"""
        if 'entity_furniture_making' in self.tip_dogovora:
            return 'на изготовление мебели'
        if 'entity_householdtec' in self.tip_dogovora:
            return 'М бытовая техника юр. лица'
        if 'entity_connectiontec' in self.tip_dogovora:
            return 'М подключение техники юр. лица'
        if 'entity_mattresses' in self.tip_dogovora:
            return 'М матрасы юр. лица'
        if 'entity_finishedfur' in self.tip_dogovora:
            return 'М  выставочного образца юр. лица'
        if 'entity_stone' in self.tip_dogovora:
            return 'на изготовление изделий из искусственного камня'
        if 'entity_textile' in self.tip_dogovora:
            return 'М на изготовление текстильных изделий и сопутствующих услуг юр. лица'
        if 'entity_transport' in self.tip_dogovora:
            return 'М транспортные услуги юр. лица'
        if 'entity_assembling' in self.tip_dogovora:
            return 'М Монтаж/демонтаж юр. лица'
        if 'entity_furnitureassemblywork' in self.tip_dogovora:
            return 'М Выполнение работ по сборке мебели юр. лица'

        """ДОГОВОРЫ С ЮР. ЛИЦАМИ ООО Фабрика мебели «Реформа»"""
        if self.tip_dogovora == 'juridical_furniture_making_fabrika_mebeli_reforma':
            return 'на изготовление мебели'
        if self.tip_dogovora == 'juridical_householdtec_fabrika_mebeli_reforma':
            return 'М бытовая техника юр. лица'
        if self.tip_dogovora == 'juridical_connectiontec_fabrika_mebeli_reforma':
            return 'М подключение техники юр. лица'
        if self.tip_dogovora == 'juridical_mattresses_fabrika_mebeli_reforma':
            return 'М матрасы юр. лица'
        if self.tip_dogovora == 'juridical_finishedfur_fabrika_mebeli_reforma':
            return 'М  выставочного образца юр. лица'
        if self.tip_dogovora == 'juridical_stone_reforma_fabrika_mebeli_reforma':
            return 'на изготовление изделий из искусственного камня'
        if self.tip_dogovora == 'juridical_textile_reforma_fabrika_mebeli_reforma':
            return 'М на изготовление текстильных изделий и сопутствующих услуг юр. лица'
        if self.tip_dogovora == 'juridical_transport_reforma_fabrika_mebeli_reforma':
            return 'М транспортные услуги юр. лица'
        if self.tip_dogovora == 'juridical_assembling_reforma_fabrika_mebeli_reforma':
            return 'М Монтаж/демонтаж юр. лица'
        if self.tip_dogovora == 'juridical_furnitureassemblywork_fabrika_mebeli_reforma':
            return 'М Выполнение работ по сборке мебели юр. лица'

        # ДОГОВОРЫ С ЮР. ЛИЦАМИ ООО «Ре-фабрик» Москва
        if self.tip_dogovora == 'juridical_moscow_ooo-refabrik_furniture_making':
            return 'М на изготовление мебели'
        if self.tip_dogovora == 'juridical_moscow_ooo-refabrik_householdtec':
            return 'М бытовая техника юр. лица'
        if self.tip_dogovora == 'juridical_ooo-refabrik_mattresses':
            return 'М матрасы юр. лица'
        if self.tip_dogovora == 'juridical_ooo-refabrik_finishedfur':
            return 'М  мебель выставочного образца юр. лица'
        if self.tip_dogovora == 'juridical_ooo-refabrik_stone':
            return 'М на изготовление изделий из искусственного камня'
        if self.tip_dogovora == 'juridical_moscow_ooo-refabrik_furnitureassemblywork':
            return 'М Выполнение работ по сборке мебели юр. лица'
        if self.tip_dogovora == 'juridical_moscow_ooo-refabrik_textile':
            return 'М на изготовление текстильных изделий и сопутствующих услуг юр. лица'

    def kakoe_yur_lico_na_kirillice(self):
        if 'fabrika_mebeli_reforma' in self.tip_dogovora:
            return 'ООО фабрика мебели «Реформа»'
        elif 'ooo_refabrik' in self.tip_dogovora:
            return 'ООО «Ре--фабрик»'
        elif 'ooo-refabrik' in self.tip_dogovora:
            return 'ООО «Ре-фабрик»'
        elif 'ooo_reforma_plus' in self.tip_dogovora or 'ooo_re_forma_plus' or 're_forma_plus_ooo' in self.tip_dogovora:
            return 'ООО «Ре-форма плюс»'
        elif 'ooo_reforma_sever' in self.tip_dogovora:
            return 'ООО «Ре-форма Север»'

        return ''

    def postavshik(self):
        postavshik = {}
        postavshik['otkaz'] = {}
        if 'reforma_plus_ooo' in self.tip_dogovora:
            postavshik['fio'] = 'ООО "Ре-форма плюс"'
            postavshik['adres1'] = '450022, Республика Башкортостан, '
            postavshik['adres2'] = 'г.Уфа, ул.Менделеева, д.145, пом. 25'
            postavshik['inn'] = '0278925778'
            postavshik['kpp'] = '027801001'
            postavshik['ogrn'] = '1160280136830'
            postavshik['rs'] = '40702810806000020287'
            postavshik['otkaz']['mygkaya_mebel'] = '450055, РБ, г. Уфа, пр. Октября, д. 170'
            postavshik['otkaz']['izgotovlenie_mebeli'] = '450055, РБ, г. Уфа, пр. Октября, д. 170'
            postavshik['otkaz']['dveri'] = '450055, РБ, г. Уфа, пр. Октября, д. 170'
        elif 'fabrika_mebeli_reforma' in self.tip_dogovora:
            postavshik['fio'] = 'ООО Фабрика мебели "Реформа"'
            postavshik['adres1'] = '450106, Республика Башкортостан, '
            postavshik['adres2'] = 'г.Уфа, ул.Менделеева, д. 128, корп. 1, этаж 1'
            postavshik['adres1_post'] = '450106, Республика Башкортостан, '
            postavshik['adres2_post'] = 'г.Уфа, ул.Менделеева, д. 128, корп. 1, этаж 1'
            postavshik['inn'] = '0274975200'
            postavshik['kpp'] = '027401001'
            postavshik['ogrn'] = '1220200035010'
            postavshik['rs'] = '40702810506000059574'
            postavshik['otkaz']['mygkaya_mebel'] = '450106, РБ, г. Уфа, ул. Менделеева, д. 128, корп. 1, этаж 1'
            postavshik['otkaz']['izgotovlenie_mebeli'] = '450106, РБ, г. Уфа, ул. Менделеева, д. 128, корп. 1, этаж 1'
            postavshik['otkaz']['dveri'] = '450106, РБ, г. Уфа, ул. Менделеева, д. 128, корп. 1, этаж 1'
        else:
            postavshik['fio'] = '___ ____ ___________'
            postavshik['svidetelstvo'] = ''
            postavshik['adres1'] = '__________________'
            postavshik['adres2'] = '__________________'
            postavshik['adres1_post'] = '__________________'
            postavshik['adres2_post'] = '__________________'
            postavshik['inn'] = '__________________'
            postavshik['ogrnip'] = '__________________'
            postavshik['rs'] = '__________________'
            postavshik['doverennost'] = '__________________'

        postavshik['nomer_dog'] = postavshik['fio'][0]
        postavshik['bank1'] = 'БАШКИРСКОЕ ОТДЕЛЕНИЕ № 8598'
        postavshik['bank2'] = 'ПАО СБЕРБАНК г. УФА'
        postavshik['ks'] = '30101810300000000601'
        postavshik['bik'] = '048073601'
        inicialy = postavshik['fio'].split(' ')
        postavshik['inicialy'] = inicialy[0] + ' ' + inicialy[1][0:1] + '.' + inicialy[2][0:1] + '.'
        return postavshik
