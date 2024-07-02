from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from .models import Account

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('access')
        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                request.user = Account.objects.get(id=user_id)
            except Exception as e:
                request.user = AnonymousUser()