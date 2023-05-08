from django.db import models
from django.contrib.auth.models import User
from .client import Client


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

    uuid = models.CharField(editable=False, unique=True, max_length=40, db_index=True)
    owner = models.ForeignKey(User, related_name='froze_owner', on_delete=models.CASCADE, verbose_name="Создатель заявки")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    type_production = models.CharField(max_length=100, verbose_name="Тип изделия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заявки")
    updated_at = models.DateTimeField(auto_now=True)
    type_pay = models.CharField(max_length=30, choices=FROZE_TYPE_PAY, null=True, blank=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=11, null=True, blank=True)        # Итоговая сумма
    total_white_goods = models.DecimalField(decimal_places=2, max_digits=11, null=True, blank=True)   # Сумма за технику
    status = models.CharField(max_length=50, choices=FROZE_STATUS_CHOICES, verbose_name="Статус")

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'





