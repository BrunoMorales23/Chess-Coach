from django.urls import path
from users.views import *

urlpatterns = [
    path('register/', register_page ,name='register'),
    path('login/', login_page, name='login')
    ]