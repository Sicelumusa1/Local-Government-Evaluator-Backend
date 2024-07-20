#!/ usr/bin/python3

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import Province, Municipality, Ward, Councilor, Services, Rating, Perspective, Petition
from .serializers import ProvinceSerializer, MunicipalitySerializer, CouncilorSerializer
from .serializers import ServicesSerializer, RatingSerializer, WardSerializer, PerspectiveSerializer, PetitionSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from accounts.authentication import CustomJWTAuthentication
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404


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
        province_id = self.kwargs.get('province_id')

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
        municipality_id = self.kwargs.get('municipality_id')

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
    serializer_class = CouncilorSerializer
    authentication_classes = (CustomJWTAuthentication, )
    permission_classes = (AllowAny, )

    def get_queryset(self):
        
        # Retrieve the query parameter to determine whether to fetch best or worst rated councilors
        rating_type = self.request.query_params.get('rating_type')

        if rating_type == 'best':
            # Fetch best rated councilors based on average rating >=4
            queryset = Councilor.objects.annotate(avg_rating=Avg('rating__stars')).filter(avg_rating__gte=4)
        elif rating_type == 'worst':
            # Fetch worst rated councilors based on average rating < 3 or None
            queryset = Councilor.objects.annotate(avg_rating=Avg('rating__stars')).filter(Q(avg_rating__lt=3) | Q(avg_rating=None))
        else:
            # Retrieve the ward_number from the query parameters      
            ward_number = self.kwargs.get('ward_number')

            # Filter the councilor based on the provided parameters
            if ward_number:
                queryset = Councilor.objects.filter(ward__ward_number=ward_number)
            else:
                queryset = Councilor.objects.all()
        return queryset
            
    # Custom rating method
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def rate_councilor(self, request, pk=None):
        if 'service' in request.data and 'stars' in request.data:

            councilor = Councilor.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            feedback = request.data.get('feedback', None)
            service_id = request.data.get('service')

            
            # Check if the user is trying to rate their councilor or not
            user_councilor = request.user.councilor
            if user_councilor == councilor:
               
                # Allow the rating
                pass
            else:
                # Reject the rating
                response = {'message': "This is not your councilor, you can't rate them."}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user has already rated this councilor for this service
            existing_rating = Rating.objects.filter(user=user, councilor=councilor, service_id=service_id).first()
            
            if existing_rating:
                
                # Check if at least 3 months have passed since the last rating
                last_rating_date = existing_rating.updated_at
                current_date = timezone.now()
                days_left = (last_rating_date + timedelta(days=90) - current_date).days
                if current_date - last_rating_date < timedelta(days=90):
                    response = {'message': f'You can only update your rating for this service once in 3 months. Please try again after {days_left} days.'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
                # Update the existing rating
                existing_rating.stars = stars
                existing_rating.feedback = feedback
                existing_rating.save()
                serializer = RatingSerializer(existing_rating, many=False)
                response = {'message': 'Rating updated successfully', 'result': serializer.data}
            else:
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
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def create(self, request, *args, **kwargs):
        response = {'message': 'Not the best way to create a rating'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Not the best way to update a rating'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
class PerspectiveViewSet(viewsets.ModelViewSet):
    queryset = Perspective.objects.all()
    serializer_class = PerspectiveSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        queryset = super().get_queryset()
        ward_id = self.queryset.query_params.get('ward', None)
        if ward_id:
            queryset = queryset.filter(ward_id=ward_id)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        ward = user.ward

        if not ward:
            response = {'message': 'You do not belong to any ward.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure that the perspective is created in the user's own ward
        if serializer.validated_data.get('ward') != ward:
            response = {'message': 'This is not your ward.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=user, ward=ward)

class PetitionViewSet(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        ward_id = self.queryset.query_params.get('ward', None)
        if ward_id:
            queryset = queryset.filter(ward_id=ward_id)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        ward = user.ward

        if not ward:
            response = {'message': 'You do not belong to any ward. Please Login'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure that the petition is created in the user's own ward
        if serializer.validated_data.get('ward') != ward:
            response = {'message': 'This is not your ward.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure that there is only one petition per ward
        existing_petition = Petition.objects.filter(ward=ward, status='active').first()
        if existing_petition:
            response = {'message': 'There is already an active petition in your ward.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=user, ward=ward)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def sign_petition(self, request, pk=None):
        petition = get_object_or_404(Petition, pk=pk)
        user = request.user

        # Ensure only residents on the ward can sign the petition
        if user.ward != petition.ward:
            response = {'message': 'You can only sign petitions in your ward'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user has not already signed the petition
        if petition.signatures.filter(id=user.id).exists():
            response = {'message': 'You have already signed this petition'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        petition.signatures.add(user)
        response = {'message': 'Petition signed successfully'}
        return Response(response, status=status.HTTP_200_OK)