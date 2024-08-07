#!/usr/bin/python3

"""
Serializers for converting complex data types (such as models) to and from native python data types.

This module defines serializers for the followig models:
- Userserializer: Serializer for the User model from Django's Authetication framework.
                    It includes fields for user edentification and password.
- PrivinceSerializer: Serializer for the Province model, representing municipal subdivisions.
- WardSerializer: Serializer for the Ward model, representing electoral divisions within municipalities.
- CouncilorSerializer: Serializer for the Councilor model, representing elected counsilors.
- ServicesSerializer: Serializer for the Rating model, representating rating associated with services.

Each serializer is a subclass of rest_framework. serializers.ModelSerializer and specifies the model and fields to include or exclude duing serialization and deserialization.
"""
from rest_framework import serializers
from .models import Province, Municipality, Ward, Councilor, Services, Rating, Perspective, Petition


class ProvinceSerializer(serializers.ModelSerializer):

    petition_count = serializers.SerializerMethodField()
    class Meta:
        model = Province
        fields = ('id', 'name', 'petition_count')
    
    def get_petition_count(self, obj):
        return obj.petition_count()


class MunicipalitySerializer(serializers.ModelSerializer):

    petition_count = serializers.SerializerMethodField()
    class Meta:
        model = Municipality
        fields = ('id', 'name', 'province', 'petition_count')
    
    def get_petition_count(self, obj):
        return obj.petition_count()


class WardSerializer(serializers.ModelSerializer):
    
    petition = serializers.SerializerMethodField()
    class Meta:
        model = Ward
        fields = ('id', 'ward_number', 'municipality', 'petition')
    
    def get_petition(self, obj):
        petition = obj.petition()
        if petition:
            return PetitionSerializer(petition).data
        return None


class CouncilorSerializer(serializers.ModelSerializer):
    names = serializers.CharField(max_length=100, required=True)
    surname = serializers.CharField(max_length=100, required=True)
    ward_number = serializers.SerializerMethodField()

    class Meta:
        model = Councilor
        fields = ('id', 'names', 'surname', 'ward_number', 'affiliation', 'no_of_ratings', 'avg_ratings')

    def get_ward_number(self, obj):
        if obj.ward:
            return obj.ward.ward_number
        else:
            return None


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('id', 'service_name')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'stars', 'councilor', 'service', 'section_or_area', 'quarter', 'year', 'feedback')

class PerspectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perspective
        fields = '__all__'
        read_only_fields = ('user', 'ward')
class PetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petition
        fields = ('id', 'title', 'description', 'user', 'ward', 'signatures', 'status')