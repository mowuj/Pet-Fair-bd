from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, activate, ProfileUpdateView, change_pass, user_logout,AdminHomeView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('admin/', AdminHomeView.as_view(), name='admin_home'),
    path('change_pass/', change_pass, name='change_pass'),
    path('edit_profile/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('active/<uid64>/<token>/',activate, name='activate'),
]
