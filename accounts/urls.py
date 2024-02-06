from django.urls import path
from .views import SignupUserView, VerifyEmail,LoginView

urlpatterns = [
    path('signup/', SignupUserView.as_view(), name='signup'),
    path('verify_email/', VerifyEmail.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', views.logout, name='logout'),
]