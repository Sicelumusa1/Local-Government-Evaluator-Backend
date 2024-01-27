from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import CouncilorViewSet, ServicesViewSet, RatingViewSet

router = routers.DefaultRouter()
router.register('Councilor', CouncilorViewSet)
router.register('Services', ServicesViewSet)
router.register('Rating', RatingViewSet)

urlpatterns = [
    path('', include(router.urls))
]
