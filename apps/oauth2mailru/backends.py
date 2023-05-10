from django.contrib.auth.models import User


class MailRuBackend(object):
    def authenticate(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
