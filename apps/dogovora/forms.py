from django import forms

from apps.dogovora.models import DogovorIndi, DogovorEntry

SPOSOB_OPLATY = (
    ('', '--способ оплаты--'),
    ('cash', 'Оплата наличными'),
    ('cash_discont', 'Наличные-скидка'),
    ('card', 'Оплата картой / Терминал'),
    ('installment', 'Рассрочка'),
    ('internal_installment', 'Внутренняя рассрочка'),
    ('perechislenie', 'Перечисление'),
)


class DogovorIndiForm(forms.Form):
    tip_dogovora = forms.ChoiceField(
        required=False, label='Тип договора', choices=(('', '--выбрать тип договора--'),) + DogovorIndi.TIPY_DOGOVOROV,
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Тип договора'}))
    technics_sroki_dostavki_tehniki = forms.ChoiceField(
        required=False, label='Сроки доставки техники/матраса', choices=(
            ('', '--выбери срок доставки--'),
            ('1', 'в день исполнения обязательств по договору'),
            ('2', 'в течении ___ рабочих дней со дня заключения Договора')
        ),
        widget=forms.Select(attrs={'class': 'form-select'}))
    technics_sroki_dostavki_tehniki_v_dnyah = forms.IntegerField(
        required=False, max_value=365, min_value=0, label='Сроки доставки техники/матраса в днях',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3'}))
    nomer_dogovora = forms.CharField(
        required=False, max_length=20, label='Номер договора',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер договора (без буквы юр.лица)', 'disabled': 'disabled'}))
    drugoy_dogovor = forms.CharField(
        required=False, max_length=20, label='№ договора на изготовление мебели',
        widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled',
                                      'placeholder': '№ договора на изготовление мебели (для пункта 3.2.)'}))
    sposob_oplaty = forms.ChoiceField(
        required=False, label='Способ оплаты', choices=SPOSOB_OPLATY,
        widget=forms.Select(attrs={'class': 'form-control'}))
    tip_opisanie_izdeliya = forms.CharField(
        required=False, max_length=500, label='Тип (описание) изделия',
        widget=forms.TextInput(attrs={'class': 'form-control type_production', 'placeholder': 'Тип (описание) изделия'}))
    passport_familiya = forms.CharField(
        required=False, max_length=200, label='Фамилия заказчика',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    passport_imya = forms.CharField(
        required=False, max_length=200, label='Имя заказчика',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    passport_otchestvo = forms.CharField(
        required=False, max_length=200, label='Отчество заказчика',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}))
    passport_birthday_date = forms.DateField(
        required=False, input_formats=['%d.%m.%Y'], initial="", label='Дата рождения',
        widget=forms.TextInput(attrs={'class': 'form-control dogovora_dates', 'placeholder': '11.10.1990', 'data-inputmask-alias': 'dd.mm.yyyy'}))
    passport_birthday_place = forms.CharField(
        required=False, max_length=200, label='Место рождения',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ГОР. УФА'}))
    passport_seria = forms.CharField(
        required=False, max_length=4, label='Серия паспорта',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '8000'}))
    passport_nomer = forms.CharField(
        required=False, max_length=6, label='Номер паспорта',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123456'}))
    passport_kem_vydan = forms.CharField(
        required=False, max_length=200, label='Кем выдан',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ОТДЕЛОМ УФМС'}))
    passport_kogda_vydan = forms.DateField(
        required=False, input_formats=['%d.%m.%Y'], initial="", label='Дата выдачи',
        widget=forms.TextInput(attrs={'class': 'form-control dogovora_dates', 'placeholder': '11.10.1990', 'data-inputmask-alias': 'dd.mm.yyyy'}))
    passport_kp = forms.CharField(
        required=False, max_length=7, label='Код подразделения',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000-111', 'data-inputmask-mask': '999-999'}))
    adres_propiski = forms.CharField(
        required=False, max_length=200, label='Почтовый идекс, Адрес прописки',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес прописки'}))
    adres_ustanovki = forms.CharField(
        required=False, max_length=200, label='Адрес установки',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес установки'}))
    vsego_k_oplate = forms.IntegerField(
        required=False, max_value=2147483647, min_value=0, label='Всего к оплате в рублях',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100000',
                                      'title': 'Итоговая сумма договора по товарному чеку, цифрами',
                                      'onkeyup': 'oplata_predoplata_and_ostatok();'}))
    oplata_predoplata_rub = forms.IntegerField(
        required=False, max_value=2147483647, min_value=0, label='Сумма предоплаты в рублях',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '70000', 'onkeyup': 'oplata_predoplata_and_ostatok();'}))
    naimenov_soputstv_izdeliy = forms.CharField(
        required=False, max_length=200, label='Наименования сопутствующих изделий',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наименования сопутствующих изделий'}))
    summa_za_soputstv_uslugi = forms.IntegerField(
        required=False, max_value=2147483647, min_value=0, label='Сумма за сопутств.услуги (если они есть)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '85000'}))
    stoimost_dostavki_vne_ufa = forms.IntegerField(
        required=False, min_value=0, max_value=2147483647, label='Стоимость доставки',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    srok_ispolneniya_rabot = forms.IntegerField(
        required=False, max_value=32767, min_value=0, label='Срок исполнения работ',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '30'}))
    installment_plan = forms.IntegerField(
        required=False, max_value=32767, min_value=0, label='Срок внутренней рассрочки',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '6'}))
    data_podpisaniya = forms.DateField(
        required=False, input_formats=['%d.%m.%Y'], initial="", label='Дата подписания',
        widget=forms.TextInput(attrs={'class': 'form-control dogovora_dates', 'placeholder': '01.06.2022', 'data-inputmask-alias': 'dd.mm.yyyy'}))
    nachalo_rabot_data = forms.DateField(
        required=False, input_formats=['%d.%m.%Y'], initial="", label='Начало работ',
        widget=forms.TextInput(attrs={'class': 'form-control dogovora_dates', 'placeholder': '01.06.2022', 'data-inputmask-alias': 'dd.mm.yyyy'}))
    okonchanie_rabot_data = forms.DateField(
        required=False, input_formats=['%d.%m.%Y'], initial="", label='Окончание работ',
        widget=forms.TextInput(attrs={'class': 'form-control dogovora_dates', 'placeholder': '01.06.2022', 'data-inputmask-alias': 'dd.mm.yyyy'}))
    doverennye_lica = forms.CharField(
        required=False, max_length=500, label='Доверенные лица',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Доверенные лица (через запятую)'}))
    doverennye_lica_telefony = forms.CharField(
        required=False, max_length=500, label='Телефоны доверенных лиц',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефоны доверенных лиц (через запятую)'}))

    def clean(self):
        def vsego_k_oplate_and_oplata_predoplata_rub_odnovremenno():
            if (self.cleaned_data.get('oplata_predoplata_rub') is not None and self.cleaned_data.get(
                    'vsego_k_oplate') is None) or (self.cleaned_data.get('oplata_predoplata_rub') is None and self.cleaned_data.get('vsego_k_oplate') is not None):
                msg = 'Поля "Всего к оплате в рублях" и "Сумма предоплаты в рублях" должны' \
                      ' заполняться одновременно'
                self.add_error('vsego_k_oplate', msg)
                self.add_error('oplata_predoplata_rub', msg)

        # По договору на оказание транспортных услуг предоплата должна быть равна 50% от суммы к оплате
        if self.cleaned_data.get('tip_dogovora') is not None and \
                self.cleaned_data.get('tip_dogovora') == 'delivery_ip_bagautdinov' or \
                self.cleaned_data.get('tip_dogovora') == 'delivery_ip_frolov' or \
                self.cleaned_data.get('tip_dogovora') == 'delivery_ip_sadykov' or \
                self.cleaned_data.get('tip_dogovora') == 'delivery_ip_hafizov' or \
                self.cleaned_data.get('tip_dogovora') == 'm_transport_ip_frolov' or \
                self.cleaned_data.get('tip_dogovora') == 'm_transport_ip_bagautdinov' or \
                self.cleaned_data.get('tip_dogovora') == 'm_transport_ip_sadykov' or \
                self.cleaned_data.get('tip_dogovora') == 'm_transport_ip_hafizov' or \
                self.cleaned_data.get('tip_dogovora') == 'm_transport_ip_usmanov':
            vsego_k_oplate_and_oplata_predoplata_rub_odnovremenno()

        # По договору на изготовление предоплата должна быть равна 50% от суммы к оплате
        if self.cleaned_data.get('tip_dogovora') is not None and \
                self.cleaned_data.get('tip_dogovora') == 'izgotovlenie_2021_02_mebeli_ip_bagautdinov' or \
                self.cleaned_data.get('tip_dogovora') == 'izgotovlenie_2021_02_mebeli_ip_sadykov' or \
                self.cleaned_data.get('tip_dogovora') == 'izgotovlenie_2021_02_mebeli_ip_hafizov' or \
                self.cleaned_data.get('tip_dogovora') == 'izgotovlenie_2021_02_mebeli_ip_chuchelenko':
            vsego_k_oplate_and_oplata_predoplata_rub_odnovremenno()

        if self.cleaned_data.get('tip_dogovora') is not None and self.cleaned_data.get('tip_dogovora') in \
                ('technic_2021_04_ip_frolov',
                 'technic_2021_04_ip_bagautdinov',
                 'technic_2021_04_ip_sadykov',
                 'technic_2021_04_ip_hafizov',
                 'm_householdtec_ip_frolov',
                 'm_householdtec_ip_bagautdinov',
                 'm_householdtec_ip_sadykov',
                 'm_householdtec_ip_hafizov',
                 'm_householdtec_ip_usmanov') and \
                bool(self.cleaned_data.get('technics_sroki_dostavki_tehniki')) is False:
            self.add_error('technics_sroki_dostavki_tehniki', 'Нужно выбрать сроки доставки техники')

        return self.cleaned_data

    class Media:
        css = {
            'all': (
                'datetimepicker/jquery.datetimepicker.css',
                'datetimepicker/suggestions.min.css',

            )
        }
        js = (
            'jquery/jquery-3.6.1.min.js',
            'datetimepicker/jquery.datetimepicker.js',
            'datetimepicker/jquery.suggestions.min.js',
            'dogovora/suggestions_dogovora.js',
        )


class DogovorFormEntry(forms.Form):
    tip_dogovora = forms.ChoiceField(
        required=False, label='Тип договора', choices=(('', '--выбрать тип договора--'),) + DogovorEntry.TIPY_DOGOVOROV,
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Тип договора'}))
    technics_sroki_dostavki_tehniki = forms.ChoiceField(
        required=False, label='Сроки доставки техники/матраса', choices=(
            ('', '--выбери срок доставки--'),
            ('1', 'в день исполнения обязательств по договору'),
            ('2', 'в течении ___ рабочих дней со дня заключения Договора')
        ),
        widget=forms.Select(attrs={'class': 'form-select'}))
    technics_sroki_dostavki_tehniki_v_dnyah = forms.IntegerField(
        required=False, max_value=365, min_value=0, label='Сроки доставки техники/матраса в днях',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3'}))
    nomer_dogovora = forms.CharField(
        required=False, max_length=20, label='Номер договора',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер договора (без буквы юр.лица)', 'disabled': 'disabled'}))
    drugoy_dogovor = forms.CharField(
        required=False, max_length=20, label='№ договора на изготовление мебели',
        widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled',
                                      'placeholder': '№ договора на изготовление мебели (для пункта 3.2.)'}))
    sposob_oplaty = forms.ChoiceField(
        required=False, label='Способ оплаты', choices=SPOSOB_OPLATY,
        widget=forms.Select(attrs={'class': 'form-control'}))
    tip_opisanie_izdeliya = forms.CharField(
        required=False, max_length=500, label='Тип (описание) изделия',
        widget=forms.TextInput(attrs={'class': 'form-control type_production', 'placeholder': 'Тип (описание) изделия'}))
    passport_familiya = forms.CharField(
        required=False, max_length=200, label='Фамилия заказчика/Название Компаний',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия/Название'}))
    passport_imya = forms.CharField(
        required=False, max_length=200, label='Имя заказчика',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    passport_otchestvo = forms.CharField(
        required=False, max_length=200, label='Отчество заказчика',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}))




    adres_propiski = forms.CharField(
        required=False, max_length=200, label='Почтовый идекс, Юр.адрес /Адрес прописки',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес прописки'}))
    general_director = forms.CharField(
        required=False, max_length=200, label='ФИО представителя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия Имя Отчество в родительном падеже'}))
    job_title = forms.CharField(
        required=False, max_length=200, label='Должность',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Должность в родительном падеже'}))
    letter_of_attorney = forms.CharField(
        required=False, max_length=200, label='Доверенность(если применимо)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '№ и дата доверенности'}))
    tax_identification_number = forms.CharField(
        required=False, max_length=12, label='ИНН',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'введите ИНН юрлица/ИП'}))
    registration_reason_code = forms.CharField(
        required=False, max_length=9, label='КПП',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'введите КПП юрлица(для ИП, не применимо)'}))
    registration_number = forms.CharField(
        required=False, max_length=15, label='ОГРН /ОГРНИП',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'введите номер юрлица/ИП'}))
    checking_account = forms.CharField(
        required=False, max_length=20, label='Номер счёта',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '20 значный расчетный счёт'}))
    account_bank = forms.CharField(
        required=False, max_length=200, label='БАНК',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'название банка'}))
    correspondent_account = forms.CharField(
        required=False, max_length=20, label='Корреспондентский счёт',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'корреспондентский счёт'}))
    bank_identification_code = forms.CharField(
        required=False, max_length=9, label='БИК организаций',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'БИК организаций'}))
    adres_ustanovki = forms.CharField(
        required=False, max_length=200, label='Адрес установки',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес установки'}))
    vsego_k_oplate = forms.IntegerField(
        required=False, max_value=2147483647, min_value=0, label='Всего к оплате в рублях',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100000',
                                      'title': 'Итоговая сумма договора по товарному чеку, цифрами',
                                      'onkeyup': 'oplata_predoplata_and_ostatok();'}))
    oplata_predoplata_rub = forms.IntegerField(
        required=False, max_value=2147483647, min_value=0, label='Сумма предоплаты в рублях',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '70000', 'onkeyup': 'oplata_predoplata_and_ostatok();'}))
    naimenov_soputstv_izdeliy = forms.CharField(
        required=False, max_length=200, label='Наименования сопутствующих изделий',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наименования сопутствующих изделий'}))
    summa_za_soputstv_uslugi = forms.IntegerField(
        required=False, max_value=2147483647, min_value=0, label='Сумма за сопутств.услуги (если они есть)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '85000'}))
    stoimost_dostavki_vne_ufa = forms.IntegerField(
        required=False, min_value=0, max_value=2147483647, label='Стоимость доставки',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    srok_ispolneniya_rabot = forms.IntegerField(
        required=False, max_value=32767, min_value=0, label='Срок исполнения работ',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '30'}))
    installment_plan = forms.IntegerField(
        required=False, max_value=32767, min_value=0, label='Срок внутренней рассрочки',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '6'}))
    data_podpisaniya = forms.DateField(
        required=False, input_formats=['%d.%m.%Y'], initial="", label='Дата подписания',
        widget=forms.TextInput(attrs={'class': 'form-control dogovora_dates', 'placeholder': '01.06.2022', 'data-inputmask-alias': 'dd.mm.yyyy'}))
    nachalo_rabot_data = forms.DateField(
        required=False, input_formats=['%d.%m.%Y'], initial="", label='Начало работ',
        widget=forms.TextInput(attrs={'class': 'form-control dogovora_dates', 'placeholder': '01.06.2022', 'data-inputmask-alias': 'dd.mm.yyyy'}))
    okonchanie_rabot_data = forms.DateField(
        required=False, input_formats=['%d.%m.%Y'], initial="", label='Окончание работ',
        widget=forms.TextInput(attrs={'class': 'form-control dogovora_dates', 'placeholder': '01.06.2022', 'data-inputmask-alias': 'dd.mm.yyyy'}))
    doverennye_lica = forms.CharField(
        required=False, max_length=500, label='Доверенные лица',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Доверенные лица (через запятую)'}))
    doverennye_lica_telefony = forms.CharField(
        required=False, max_length=500, label='Телефоны доверенных лиц',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефоны доверенных лиц (через запятую)'}))


    def clean(self):
        def vsego_k_oplate_and_oplata_predoplata_rub_odnovremenno():
            if (self.cleaned_data.get('oplata_predoplata_rub') is not None and self.cleaned_data.get('vsego_k_oplate') is None) \
                    or (self.cleaned_data.get('oplata_predoplata_rub') is None and self.cleaned_data.get('vsego_k_oplate') is not None) :
                msg = 'Поля "Всего к оплате в рублях" и "Сумма предоплаты в рублях" должны' \
                      ' заполняться одновременно'
                self.add_error('vsego_k_oplate', msg)
                self.add_error('oplata_predoplata_rub', msg)

        # По договору на оказание транспортных услуг предоплата должна быть равна 50% от суммы к оплате
        if self.cleaned_data.get('tip_dogovora') is not None and \
                self.cleaned_data.get('tip_dogovora') == 'entity_transport_reforma_plus_ooo' or \
                self.cleaned_data.get('tip_dogovora') == 'juridical_transport_reforma_fabrika_mebeli_reforma' or \
                self.cleaned_data.get('tip_dogovora') == 'entity_ufa_transport_fabrika_mebeli_reforma':
            vsego_k_oplate_and_oplata_predoplata_rub_odnovremenno()

        # По договору на оказание транспортных услуг предоплата должна быть равна 50% от суммы к оплате
        if self.cleaned_data.get('tip_dogovora') is not None and \
                self.cleaned_data.get('tip_dogovora') == 'izgotovlenie_2019_11_mebeli_ip_bagautdinov' or \
                self.cleaned_data.get('tip_dogovora') == 'izgotovlenie_2019_11_mebeli_ip_sadykov' or \
                self.cleaned_data.get('tip_dogovora') == 'izgotovlenie_2019_11_mebeli_ip_hafizov' or \
                self.cleaned_data.get('tip_dogovora') == 'izgotovlenie_2019_11_mebeli_ip_chuchelenko':
            vsego_k_oplate_and_oplata_predoplata_rub_odnovremenno()

        if self.cleaned_data.get('tip_dogovora') is not None and self.cleaned_data.get('tip_dogovora') in \
                ('technic_2021_04_ip_frolov', 'technic_2021_04_ip_bagautdinov', 'technic_2021_04_ip_sadykov',
                 'technic_2021_04_ip_hafizov', 'm_householdtec_ip_frolov', 'm_householdtec_ip_bagautdinov',
                 'm_householdtec_ip_sadykov', 'm_householdtec_ip_hafizov', 'm_householdtec_ip_usmanov',
                 'entity_householdtec_reforma_plus_ooo', 'juridical_moscow_ooo-refabrik_householdtec',
                 'juridical_householdtec_fabrika_mebeli_reforma', 'entity_ufa_householdtec_fabrika_mebeli_reforma',
                 'entity_ufa_ooo-refabrik_householdtec') and \
                bool(self.cleaned_data.get('technics_sroki_dostavki_tehniki')) is False:
            self.add_error('technics_sroki_dostavki_tehniki', 'Нужно выбрать сроки доставки техники')

        return self.cleaned_data

    class Media:
        css = {
            'all': (
                'datetimepicker/jquery.datetimepicker.css',

                'froze/suggestions-4.10.css',
                'froze/google_autocomplete/google_map_api_v3.css',
            )
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
            'datetimepicker/jquery.datetimepicker.js',

            'froze/jquery.suggestions-4.10.min.js',
            'dogovora/suggestions_dogovora.js',
        )