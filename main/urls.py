from django.contrib.auth import login
from django.urls import path, include
from . import views
from .views import MainPage , RegisterUser, LoginUser

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
]
