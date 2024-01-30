from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import CouncilorViewSet, ServicesViewSet, RatingViewSet
from .views import ProvinceViewSet, MunicipalityViewSet, UserViewSet, WardViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('provinces', ProvinceViewSet)
router.register('municipalities', MunicipalityViewSet)
router.register('wards', WardViewSet)
router.register('councilors', CouncilorViewSet)
router.register('services', ServicesViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
