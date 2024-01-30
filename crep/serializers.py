from rest_framework import serializers
from .models import Province, Municipality, Ward, Councilor, Services, Rating
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            token = Token.objects.create(user=user)
            return user


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name')


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = ('id', 'name', 'province')


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ('id', 'ward_number', 'municipality')


class CouncilorSerializer(serializers.ModelSerializer):
    names = serializers.CharField(max_length=100, required=True)
    surname = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Councilor
        fields = ('id', 'names', 'surname', 'ward', 'affiliation', 'no_of_ratings', 'avg_ratings')


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('id', 'service_name')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'stars', 'councilor', 'service', 'section_or_area', 'quarter', 'year', 'feedback')
