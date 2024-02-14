from django.contrib.auth.backends import ModelBackend
# from datetime import date
from rest_framework.authtoken.models import Token

class Autenticador(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            User = super().authenticate(request, username, password)
            if User == None:
                return None
            if User.is_superuser:
                token,created = Token.objects.get_or_create(user = User)
                return User
            if User.is_active:
                token,created = Token.objects.get_or_create(user = User)
                return User
            return None
        except User.DoesNotExist:
            return None
