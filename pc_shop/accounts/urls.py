from django.urls import path
from .views import LoginView, RegisterView, logout_view, profile_view, edit_profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]