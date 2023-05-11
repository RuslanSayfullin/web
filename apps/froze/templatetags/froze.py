from django import template
from django.contrib.auth import get_user_model

User = get_user_model()
register = template.Library()


@register.filter
def pretty_number_phone(phone):
    phone = "+" + phone
    str_phone = "+{0}({1})-{2}-{3}".format(phone[1], phone[2:5], phone[5:8], phone[8:])
    return str_phone
