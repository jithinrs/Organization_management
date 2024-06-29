from django.contrib import admin
from django.urls import path
from .views import sign_up, home_page, log_out, login_view, create_user



urlpatterns = [
    path('register/',  sign_up, name='signup'),
    path('homepage/', home_page, name='homepage'),
    path('logout/', log_out, name='logout'),
    path('login/', login_view, name='login'),
    path('create_user/', create_user, name='createuser')
]

