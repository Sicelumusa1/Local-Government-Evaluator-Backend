#!/usr/bin/python3

from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import CouncilorViewSet, ServicesViewSet, RatingViewSet
from .views import ProvinceViewSet, MunicipalityViewSet, WardViewSet

router = routers.DefaultRouter()
router.register('provinces', ProvinceViewSet)
router.register('provinces/(?P<province_pk>[^/.]+)/municipalities', MunicipalityViewSet, basename='province-municipalities')
router.register('municipalities/(?P<municipality_pk>[^/.]+)/wards', WardViewSet, basename='municipality-wards')
router.register('councilors', CouncilorViewSet)
router.register('services', ServicesViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
