import logging
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from users.permissions import *

logger = logging.getLogger(__name__)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        logger.info("Accessed Category List")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Category created by user: {request.user}")
        return super().create(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        logger.info("Accessed Product List")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Product created by user: {request.user}")
        return super().create(request, *args, **kwargs)

def product_list(request):
    products = Product.objects.all()
    logger.info(f"Product list accessed by {request.user}")
    return render(request, 'products/products_list.html', {'products': products})
