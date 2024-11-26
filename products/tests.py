from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import Role
from users.models import User
from .models import Category, Product


# Base test case with setup for admin user and JWT tokens
class BaseAPITest(APITestCase):
    def setUp(self):
        # Удаляем все записи перед началом теста
        Category.objects.all().delete()
        Product.objects.all().delete()
        Role.objects.all().delete()
        User.objects.all().delete()

        # Создаём роль "Admin"
        self.admin_role = Role.objects.create(name="Admin")

        # Создаём пользователя с ролью администратора
        self.admin_user = User.objects.create_user(
            username="admin",
            password="admin123",
            is_staff=True,
            role=self.admin_role
        )
        self.token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.auth_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }


# Tests for the Category model
class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="Devices and gadgets")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.description, "Devices and gadgets")
        self.assertEqual(str(self.category), "Electronics")


# Tests for the Product model
class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="Devices and gadgets")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest model",
            price=999.99,
            quantity=10,
            pv_points=50,
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Smartphone")
        self.assertEqual(self.product.description, "Latest model")
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.product.pv_points, 50)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(str(self.product), "Smartphone")


# Tests for the Category API
class CategoryAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        # Создаём только одну категорию для текущего теста
        self.category = Category.objects.create(name="Electronics", description="Devices and gadgets")
        self.category_url = reverse('category-list')

    def test_get_categories(self):
        response = self.client.get(self.category_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_category(self):
        data = {"name": "Furniture", "description": "Home and office furniture"}
        response = self.client.post(self.category_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.last().name, "Furniture")


# Tests for the Product API
class ProductAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        # Создаём категорию и продукт для текущего теста
        self.category = Category.objects.create(name="Electronics", description="Devices and gadgets")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest model",
            price=999.99,
            quantity=10,
            pv_points=50,
            category=self.category
        )
        self.product_url = reverse('product-list')

    def test_get_products(self):
        response = self.client.get(self.product_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_product(self):
        data = {
            "name": "Laptop",
            "description": "High performance laptop",
            "price": 1500.00,
            "quantity": 5,
            "pv_points": 100,
            "category": self.category.id
        }
        response = self.client.post(self.product_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.last().name, "Smartphone")


# Tests for the Product List View (HTML)
class ProductListViewTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Admin")
        self.category = Category.objects.create(name="Electronics", description="Devices and gadgets")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest model",
            price=999.99,
            quantity=10,
            pv_points=50,
            category=self.category
        )
        self.url = reverse('product_list')

    def test_product_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smartphone")
        self.assertContains(response, "999.99")
