import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import Account

class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Error decoding token')
        
        try:
            user = Account.objects.get(id=payload['id'])
        except Account.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
        
        return (user, None)

