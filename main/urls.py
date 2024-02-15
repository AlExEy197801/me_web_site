from django.contrib.auth import login
from django.urls import path, include
from . import views
from .views import MainPage #, RegisterUser, LoginUser

urlpatterns = [
    path('', MainPage.as_view(), name='home')
]
