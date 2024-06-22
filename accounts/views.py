from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .serializers import SignupSerializer, LoginSerializer, PasswordResetSelializer, NewPasswordSerializer
from rest_framework.response import Response
from .utils import send_pin
from .models import OTP
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.backends import TokenBackend
from .models import Account
from rest_framework.decorators import api_view, permission_classes
from crep.models import Councilor
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here.

class SignupUserView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class= SignupSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            send_pin(user['email'])
            # Send user an email
            return Response({
                'data':user,
                'message':f'Hi {user["first_name"]} Congratulations'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmail(GenericAPIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        otp_code = request.data.get('otp')
        try:
            user_code_obj = OTP.objects.get(pin=otp_code)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
                return Response({'message': 'Email verified successfilly'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Code invalid user already cerified'}, status=status.HTTP_204_NO_CONTENT)
        except OTP.DoesNotExist:
            return Response({'message': 'otp not provided'}, status=status.HTTP_404_NOT_FOUND)
        
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        
        user_data = serializer.validated_data
        access_token = user_data.get('access_token')
        refresh_token = user_data.get('refresh_token')

        response = Response({
            'message': 'Login successful',
            'email': user_data.get('email'),
            'full_name': user_data.get('full_name')
        })

        response.set_cookie(
            key='access',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='None'
        )

        response.set_cookie(
            key='refresh',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='None'
        )

        return response

class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def validate_jwt_token(token):
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=True)
            user = valid_data['user']
            return user
        except Exception as e:
            return None

    def get(self, request):
        data= {
            'message': 'Authorized'
        }
        return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def associate_user_with_councilor(request):
    try:
        user = request.user
        province = request.data.get('province')
        municipality = request.data.get('municipality')
        ward = request.data.get('ward')

        # Query the database to find the matching councilor
        councilor = Councilor.objects.get(province=province, municipality=municipality, ward=ward)

        # Update the user's Councilor field
        user.councilor = councilor
        user.save()

        return Response({'message': 'User associated with councilor successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSelializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'An email with a link to reset your password has been sent'}, status=status.HTTP_200_OK)
    

class ConfirmPasswordReset(GenericAPIView):
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user =  Account.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'Your token has expired or is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Valid credentials', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'message': 'Your token has expired or is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
class NewPassword(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = NewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':'Password reset successfull'}, status=status.HTTP_200_OK)