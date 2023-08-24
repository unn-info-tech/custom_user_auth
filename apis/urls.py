# accounts/urls.py

from django.urls import path
from .views import register_user, user_login, user_logout, delete_user, user_profile, update_profile

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('delete/', delete_user, name='delete_user'),
    path('profile/', user_profile, name='profile'),
    path('update/', update_profile, name='update'),



]