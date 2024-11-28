
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

urlpatterns = [
    path('', LoginPageView.as_view(), name='login_page'),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('register/', RegisterPageView.as_view(), name='register_page'),
    path('login/', LoginPageView.as_view(), name='login_page'),
]
