from django.urls import path
from .views import SignupUserView, VerifyEmail,LoginView, TestAuthenticationView

urlpatterns = [
    path('signup/', SignupUserView.as_view(), name='signup'),
    path('verify_email/', VerifyEmail.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', TestAuthenticationView.as_view(), name='granted'),
]