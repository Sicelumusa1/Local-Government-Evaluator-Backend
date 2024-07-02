from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken, TokenError
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
            except TokenError as e:
                print(f'Token decoding error: {e}')
                request.user = AnonymousUser()
            except Account.DoesNotExist:
                print(f'User with id {user_id} does not exist')
                request.user = AnonymousUser()
            except Exception as e:
                print(f'Unexpected error: {e}')
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()