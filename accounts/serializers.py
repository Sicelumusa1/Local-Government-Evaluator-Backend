from rest_framework import serializers
from .models import Account
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_password_reset_email

class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=100, min_length=7, write_only=True)
    password2=serializers.CharField(max_length=100, min_length=7, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'username', 'password', 'password2', 'province', 
                  'municipality', 'ward', 'councilor' ,'section_or_area']

    def validate(self, attrs):
        password= attrs.get('password', '')
        password2= attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs
    
    def create(self, validated_data):
        user=Account.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            province=validated_data.get('province'),
            municipality=validated_data.get('municipality'),
            ward=validated_data.get('ward'),
            councilor=validated_data.get('councilor'),
            section_or_area=validated_data.get('section_or_area'),
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=255, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Account
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials try again')
        if not user.is_verified:
            raise AuthenticationFailed('Invalid credentials try again')
        user_tokens = user.tokens()
        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh'))
        }
    
class PasswordResetSelializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get("email")
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            link = reverse('confirm-password-reset', kwargs={'uidb64':uidb64, 'token':token})
            password_reset_link = f"http://{site_domain}{link}"
            email_body = f"Hello, use the link below to reset your password \n {password_reset_link}"
            data = {
                'email_body': email_body,
                'email_subject': 'Reset your password',
                'to_email': user.email
            }
            send_password_reset_email(data)
        return attrs
    
class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']
    def validate(self, attrs):
        
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Link has expired ar invalid', 401)
            if password != confirm_password:
                raise AuthenticationFailed('Passwords do not match')
            user.set_password(password)
            user.save()
            return attrs
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            return AuthenticationFailed('Link has expired ar invalid')


