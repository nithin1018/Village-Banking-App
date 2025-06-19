from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterProfileView,CustomTokenObtainPairView,ProfileLogoutView,UpdatePasswordView,ForgotPasswordView,UserProfileView,AdminDashboardView

urlpatterns = [
    path("profile/register/", RegisterProfileView.as_view(),name='profile_register'),
    path('profile/login/',CustomTokenObtainPairView.as_view(),name='profile_login'),
    path('profile/login/refresh/',TokenRefreshView.as_view(),name='profile_login_refresh'),
    path('profile/logout/',ProfileLogoutView.as_view(),name='profile_logout'),
    path('profile/change-password/',UpdatePasswordView.as_view(),name='profile_change_password'),
    path('profile/login/forgot-password/',ForgotPasswordView.as_view(),name='profile_login_forgot_password'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('admin/dashboard/',AdminDashboardView.as_view(),name='admin_dashboard'),
]
