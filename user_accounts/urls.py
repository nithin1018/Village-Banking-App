from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterProfileView,CustomTokenObtainPairView,ProfileLogoutView,UpdatePasswordView,ForgotPasswordView,UserProfileView,AdminDashboardView,TransactionView,AccountProfileDetailedView,AdminDashboardUserView,AdminDashboardUserDetailedView,AdminDashboardTransactionView,AdminDashboardTransactionDetailedView

urlpatterns = [
    path("profile/register/", RegisterProfileView.as_view(),name='profile_register'),
    path('profile/login/',CustomTokenObtainPairView.as_view(),name='profile_login'),
    path('profile/login/refresh/',TokenRefreshView.as_view(),name='profile_login_refresh'),
    path('profile/logout/',ProfileLogoutView.as_view(),name='profile_logout'),
    path('profile/change-password/',UpdatePasswordView.as_view(),name='profile_change_password'),
    path('profile/login/forgot-password/',ForgotPasswordView.as_view(),name='profile_login_forgot_password'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('profile/<int:pk>/',AccountProfileDetailedView.as_view(),name='profile_detailed'),
    path('admin/dashboard/',AdminDashboardView.as_view(),name='admin_dashboard'),
    path('admin/dashboard/profile/',AdminDashboardUserView.as_view(),name='admin_dashboard_profile'),
    path('admin/dashboard/transaction/',AdminDashboardTransactionView.as_view(),name='admin_dashboard_transacation'),
    path('admin/dashboard/profile/<int:pk>/',AdminDashboardUserDetailedView.as_view(),name='admin_dashboard_profile_id'),
     path('admin/dashboard/transaction/<int:pk>/',AdminDashboardTransactionDetailedView.as_view(),name='admin_dashboard_transaction_id'),
    path('profile/transaction/',TransactionView.as_view(),name='transaction'),
]
