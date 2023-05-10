# Generated by Django 4.2.1 on 2023-05-10 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_froze', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='froze',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('pay', 'Оплатились')], default='new', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='froze',
            name='uuid',
            field=models.CharField(db_index=True, max_length=40, unique=True, verbose_name='Идентификатор'),
        ),
    ]
