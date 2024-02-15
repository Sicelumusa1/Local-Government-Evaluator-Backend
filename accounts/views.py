from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import SignupSerializer, LoginSerializer
from rest_framework.response import Response
from .utils import send_pin
from .models import OTP
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.backends import TokenBackend
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
        
class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def validate_jwt_token(token):
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user = valid_data['user']
            return user
        except Exception as e:
            return None

    def get(self, request):
        data= {
            'message': 'Authorized'
        }
        return Response(data, status=status.HTTP_200_OK)