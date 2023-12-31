from django.urls import path

from .views import ProfileUpdateView, ProfileDetailView
from .views import UserRegisterView, UserLoginView, UserLogoutView, UserPasswordChangeView




urlpatterns = [
    path('users/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('users/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),

]