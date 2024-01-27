from django.shortcuts import render
from rest_framework import viewsets
from .models import Councilor, Services, Rating
from .serializers import CouncilorSerializer, ServicesSerializer, RatingSerializer

# Create your views here.


class CouncilorViewSet(viewsets.ModelViewSet):
    queryset = Councilor.objects.all()
    serializer_class = CouncilorSerializer


class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
