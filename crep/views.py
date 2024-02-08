#!/ usr/bin/python3

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Province, Municipality, Ward, Councilor, Services, Rating
from .serializers import ProvinceSerializer, MunicipalitySerializer, CouncilorSerializer
from .serializers import ServicesSerializer, RatingSerializer, WardSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
# Create your views here.


class ProvinceViewSet(viewsets.ModelViewSet):
    """
    Manages geographic provinces.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = (AllowAny,)


class MunicipalityViewSet(viewsets.ModelViewSet):
    """
    Manages municipal subdivisions within provices.
    """
    serializer_class = MunicipalitySerializer
    permission_classes = (AllowAny,)
    # queryset = Municipality.objects.all()

    def get_queryset(self):
        # Retrieve the province_id from the query parameters
        province_id = self.request.query_params.get('province_id')

        # Filter the municipalities based on the specified province
        if province_id:
            queryset = Municipality.objects.filter(province=province_id)
        else:
            queryset = Municipality.objects.all()
        return queryset


class WardViewSet(viewsets.ModelViewSet):
    """
    Manages electoral divisions within municipalities.
    """
    serializer_class = WardSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        # Retrieve the municipality_id from the query parameters
        municipality_id = self.request.query_params.get('municipality_id')

        # Filter the municipalities based on the specified province
        if municipality_id:
            queryset = Ward.objects.filter(municipality=municipality_id)
        else:
            queryset = Ward.objects.all()
        return queryset


class CouncilorViewSet(viewsets.ModelViewSet):
    """
    Manages elected councilors within wards.
    """
    queryset = Councilor.objects.all()
    serializer_class = CouncilorSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

    def get_queryset(self):
        # Retrieve the ward_number from the query parameters
        queryset = super().get_queryset()       
        ward_number = self.request.query_params.get('ward_number')

        # Filter the councilor based on the specified ward number
        if ward_number:
            queryset = Councilor.objects.filter(ward__ward_number=ward_number)
        return queryset
        
    # Custom rating method

    @action(detail=True, methods=['POST'])
    def rate_councilor(self, request, pk=None):
        if 'service' in request.data and 'stars' in request.data:

            councilor = Councilor.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            feedback = request.data.get('feedback', None)
            service_id = request.data.get('service')
            # print('user', user.username)
            # print('Councilor ID', councilor.id)
            # print('Stars', stars)
            # print('Service ID', service_id)

            try:
                rating = Rating.objects.get(user=user.id, councilor=councilor.id, service_id=service_id)
                rating.stars = stars
                rating.feedback = feedback
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, councilor=councilor, service_id=service_id, stars=stars, feedback=feedback)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created successfully', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'Stars not provided'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = (AllowAny,)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def create(self, request, *args, **kwargs):
        response = {'message': 'Not the best way to create a rating'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Not the best way to update a rating'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
