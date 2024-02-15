from rest_framework import serializers
from .models import Account
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=100, min_length=7, write_only=True)
    password2=serializers.CharField(max_length=100, min_length=7, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'username', 'password', 'password2']

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
