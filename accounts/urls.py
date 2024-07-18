from django.urls import path
from .views import SignupUserView, VerifyEmail,LoginView, TestAuthenticationView, ConfirmPasswordReset, NewPassword, PasswordResetView, ProfileView

urlpatterns = [
    path('signup/', SignupUserView.as_view(), name='signup'),
    path('verify_email/', VerifyEmail.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='granted'),
    path('password_reset/', PasswordResetView.as_view(), name='password-reset'),
    path('new_password/', NewPassword.as_view(), name='new_password'),
    path('confirm_password/<uidb64>/<token>', ConfirmPasswordReset.as_view(), name='confirm-password-reset'),
]