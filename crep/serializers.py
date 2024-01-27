from rest_framework import serializers
from .models import Councilor, Services, Rating


class CouncilorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Councilor
        fields = ('id', 'names', 'surname', 'municipality', 'ward_number', 'affiliation')


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('id', 'service_name')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'stars', 'councilor', 'service', 'section_or_area', 'quarter', 'year')
