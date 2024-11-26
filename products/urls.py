from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, product_list
from django.urls import path, include

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('product-list/', product_list, name='product_list'),
]