#!/usr/bin/python3

from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import CouncilorViewSet, ServicesViewSet, RatingViewSet
from .views import ProvinceViewSet, MunicipalityViewSet, WardViewSet
from .views import PerspectiveViewSet, PetitionViewSet


router = routers.DefaultRouter()
router.register('provinces', ProvinceViewSet)
router.register(r'provinces/(?P<province_id>\d+)/municipalities', MunicipalityViewSet, basename='municipality')
router.register('municipalities', MunicipalityViewSet, basename='municipality')
router.register(r'municipalities/(?P<municipality_id>\d+)/wards', WardViewSet, basename='ward')
router.register('wards', WardViewSet, basename='ward')
router.register(r'wards/(?P<ward_number>\d+)/councilors', CouncilorViewSet, basename='councilor')
router.register('councilors', CouncilorViewSet, basename='councilor')
router.register('services', ServicesViewSet)
router.register('ratings', RatingViewSet)
router.register('perspectives', PerspectiveViewSet)
router.register('petitions', PetitionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('councilors/best/', CouncilorViewSet.as_view({'get': 'list'}), {'rating_type': 'best'}, name='best-councilors'),
    path('councilors/worst/', CouncilorViewSet.as_view({'get': 'list'}), {'rating_type': 'worst'}, name='worst-councilors'),
]
