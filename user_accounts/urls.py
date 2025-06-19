from django.urls import path
from .views import RegisterProfileView,CustomTokenObtainPairView,ProfileLogoutView,UpdatePasswordView,ForgotPasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("profile/register/", RegisterProfileView.as_view(),name='profile_register'),
    path('profile/login/',CustomTokenObtainPairView.as_view(),name='profile_login'),
    path('profile/login/refresh',TokenRefreshView.as_view(),name='profile_login_refresh'),
    path('profile/logout/',ProfileLogoutView.as_view(),name='profile_logout'),
    path('profile/change-password',UpdatePasswordView.as_view(),name='profile_change_password'),
    path('profile/login/forgot-password/',ForgotPasswordView.as_view(),name='profile_login_forgot_password'),
    
]
