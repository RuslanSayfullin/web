# Generated by Django 4.2.1 on 2023-05-08 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Froze',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(db_index=True, editable=False, max_length=40, unique=True)),
                ('name', models.CharField(max_length=100, verbose_name='ФИО/Название клиента')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес клиента')),
                ('phone', models.CharField(max_length=50, verbose_name='Телефон Клиента')),
                ('type_production', models.CharField(max_length=100, verbose_name='Тип изделия')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type_pay', models.CharField(blank=True, choices=[('cash', 'Оплата наличными'), ('cash_discont', 'Наличные-скидка'), ('card', 'Оплата картой'), ('installment', 'Банковская рассрочка'), ('internal_installment', 'Внутренняя рассрочка'), ('perechislenie', 'Перечисление')], max_length=30, null=True, verbose_name='Способ оплаты')),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True, verbose_name='Сумма за мебель')),
                ('total_white_goods', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True, verbose_name='Сумма за технику')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('pay', 'Оплатились')], max_length=50, verbose_name='Статус')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='froze_owner', to=settings.AUTH_USER_MODEL, verbose_name='Создатель заявки')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]
