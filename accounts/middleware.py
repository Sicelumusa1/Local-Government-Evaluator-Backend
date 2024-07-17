from django.utils.deprecation import MiddlewareMixin
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken
# from django.contrib.auth.models import AnonymousUser
# from .models import Account

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            