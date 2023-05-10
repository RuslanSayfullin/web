import requests

from django.conf import settings

OAUTH_MAIL_RU_CLIENT_ID = settings.OAUTH_MAIL_RU_CLIENT_ID
OAUTH_MAIL_RU_CLIENT_SECRET = settings.OAUTH_MAIL_RU_CLIENT_SECRET
OAUTH_MAIL_RU_REDIRECT_URI = settings.OAUTH_MAIL_RU_REDIRECT_URI


def get_user_uid(code):
    params = {
        'client_id': OAUTH_MAIL_RU_CLIENT_ID,
        'client_secret': OAUTH_MAIL_RU_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': OAUTH_MAIL_RU_REDIRECT_URI
    }

    res = requests.post("https://connect.mail.ru/oauth/token", data=params,
                        headers={'content-type': 'application/x-www-form-urlencoded'})
    res = res.json()
    uid = res.get('x_mailru_vid', None)
    return uid
