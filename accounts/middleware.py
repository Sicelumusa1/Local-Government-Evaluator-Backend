from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.contrib.auth.models import AnonymousUser
from .models import Account

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            try:
                token = AccessToken(access_token)
                user_id = token['user_id']
                request.user = Account.objects.get(id=user_id)
            except TokenError as e:
                print(f"Token decoding error: {e}")
                request.user = AnonymousUser()
            except Exception as e:
                print(f"Unexpected error: {e}")
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
        response = self.get_response(request)
        return response