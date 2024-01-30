from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Province, Municipality, Ward, Councilor, Services, Rating
from .serializers import ProvinceSerializer, MunicipalitySerializer, CouncilorSerializer
from .serializers import ServicesSerializer, RatingSerializer, UserSerializer, WardSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = (AllowAny,)


class MunicipalityViewSet(viewsets.ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    permission_classes = (AllowAny,)


class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = (AllowAny,)


class CouncilorViewSet(viewsets.ModelViewSet):
    queryset = Councilor.objects.all()
    serializer_class = CouncilorSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )
    # Custom rating method

    @action(detail=True, methods=['POST'])
    def rate_councilor(self, request, pk=None):
        if 'stars' in request.data:

            councilor = Councilor.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            feedback = request.data.get('feedback', None)
            service = request.data.get('service', None)
            print('user', user.username)
            print('Councilor ID', councilor.id)
            print('Stars', stars)
            print('Service ID', service)

            if service is None:
                response = {'message': 'Service to rate the councilor on is not provided'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            try:
                rating = Rating.objects.get(user=user.id, councilor=councilor.id)
                rating.stars = stars
                rating.feedback = feedback
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, councilor=councilor, stars=stars, feedback=feedback)
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
