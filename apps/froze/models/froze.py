import string

from django.db import models
from django.contrib.auth.models import User


def clean_number_phone(phone):
    phone = [n for n in phone if n in string.digits]
    return "".join(phone)


FROZE_TYPE_PAY = (
    ('cash', 'Оплата наличными'),
    ('cash_discont', 'Наличные-скидка'),
    ('card', 'Оплата картой'),
    ('installment', 'Банковская рассрочка'),
    ('internal_installment', 'Внутренняя рассрочка'),
    ('perechislenie', 'Перечисление'),
)


class Froze(models.Model):
    """Модель заявки, которая создаётся из Bitrix"""
    FROZE_NEW = 'new'
    FROZE_PAY = 'pay'

    FROZE_STATUS_CHOICES = (
        (FROZE_NEW, u'Новый'),
        (FROZE_PAY, u'Оплатились'),
    )

    uuid = models.CharField(unique=True, max_length=40, db_index=True, verbose_name="Идентификатор")

    name = models.CharField(max_length=100, verbose_name="ФИО/Название клиента")
    address = models.CharField(max_length=200, verbose_name="Адрес клиента")
    phone = models.CharField(max_length=50, verbose_name="Телефон Клиента")

    owner = models.ForeignKey(User, related_name='froze_owner', on_delete=models.CASCADE, verbose_name="Создатель заявки")
    type_production = models.CharField(max_length=100, verbose_name="Тип изделия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заявки")
    updated_at = models.DateTimeField(auto_now=True)
    type_pay = models.CharField(max_length=30, choices=FROZE_TYPE_PAY, null=True, blank=True, verbose_name="Способ оплаты")
    total_amount = models.DecimalField(decimal_places=2, max_digits=11, null=True, blank=True, verbose_name="Сумма за мебель")
    total_white_goods = models.DecimalField(decimal_places=2, max_digits=11, null=True, blank=True, verbose_name="Сумма за технику")
    status = models.CharField(max_length=50, choices=FROZE_STATUS_CHOICES, verbose_name="Статус", default='new')

    # номер договора, обновляется при сохранении договора для ЮЛ или ФЗ
    nomer_dogovora = models.CharField(max_length=20, default='', blank=True, null=True,
                                      verbose_name="Номер договора")

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def save(self, *args, **kwargs):
        self.phone = clean_number_phone(self.phone)
        super(Froze, self).save(*args, **kwargs)






