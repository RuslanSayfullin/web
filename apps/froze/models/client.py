from django.db import models
import string


def clean_number_phone(phone):
    phone = [n for n in phone if n in string.digits]
    return "".join(phone)


class Client(models.Model):
    """Модель Клиента"""
    name = models.CharField(max_length=100, verbose_name="Фамилия Имя Отчество/Название клиента")
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, verbose_name="Телефон Клиента")
    phone_two = models.CharField(max_length=50, null=True, blank=True)
    room = models.CharField(max_length=20)
    floor = models.CharField(max_length=20)
    porch = models.CharField(max_length=5, verbose_name=u"Номер подъезда", blank=True, null=True)

    class Meta:
        default_permissions = []
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __unicode__(self):
        return u"{0} {1}".format(self.name, self.address)

    def save(self, *args, **kwargs):
        self.phone = clean_number_phone(self.phone)
        if self.phone_two:
            self.phone_two = clean_number_phone(self.phone_two)
        super(Client, self).save(*args, **kwargs)
