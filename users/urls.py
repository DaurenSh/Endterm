
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('register/', RegisterPageView.as_view(), name='register_page'),  # Отображение страницы регистрации
    path('login/', LoginPageView.as_view(), name='login_page'),
]