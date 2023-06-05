from django import template

from portal import settings

register = template.Library()

OAUTH_MAIL_RU_CLIENT_ID = settings.OAUTH_MAIL_RU_CLIENT_ID
OAUTH_MAIL_RU_REDIRECT_URI = settings.OAUTH_MAIL_RU_REDIRECT_URI


@register.simple_tag
def oauth_url():
    url = "https://connect.mail.ru/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
    return url.format(client_id=OAUTH_MAIL_RU_CLIENT_ID, redirect_uri=OAUTH_MAIL_RU_REDIRECT_URI)
