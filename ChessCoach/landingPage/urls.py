from django.urls import path
from landingPage.views import landing_page

urlpatterns = [
    path('', landing_page ,name='landing')
    ]