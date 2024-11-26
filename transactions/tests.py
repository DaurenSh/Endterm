from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from users.models import Role, User
from products.models import Product, Category
from .models import Transaction


# Base test case with setup for admin user and JWT tokens
class BaseAPITest(APITestCase):
    def setUp(self):
        # Очистка базы данных
        Transaction.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        Role.objects.all().delete()

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


# Tests for the Transaction model
from django.test import TestCase
from users.models import Role, User
from products.models import Product, Category
from .models import Transaction

class TransactionModelTest(TestCase):
    def setUp(self):
        # Очистка базы данных
        Transaction.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        Role.objects.all().delete()

        # Создаём роль
        self.admin_role = Role.objects.create(name="Admin")

        # Создаём категорию, продукт и пользователя
        self.category = Category.objects.create(name="Electronics", description="Devices and gadgets")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest model",
            price=999.99,
            quantity=10,
            pv_points=50,
            category=self.category
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            role=self.admin_role
        )

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            transaction_type="acceptance",
            product=self.product,
            quantity=5,
            responsible_user=self.user
        )
        self.assertEqual(transaction.transaction_type, "acceptance")
        self.assertEqual(transaction.product, self.product)
        self.assertEqual(transaction.quantity, 5)
        self.assertEqual(transaction.responsible_user, self.user)
        self.assertIsNotNone(transaction.timestamp)



# Tests for the Transaction API
class TransactionAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        # Создаём категорию и продукт
        self.category = Category.objects.create(name="Electronics", description="Devices and gadgets")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest model",
            price=999.99,
            quantity=10,
            pv_points=50,
            category=self.category
        )
        # Эндпоинт для транзакций
        self.transaction_url = reverse('transaction-list')

    def test_create_transaction(self):
        data = {
            "transaction_type": "acceptance",
            "product": self.product.id,
            "quantity": 5,
            "responsible_user": self.admin_user.id
        }
        response = self.client.post(self.transaction_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.transaction_type, "acceptance")
        self.assertEqual(transaction.product, self.product)
        self.assertEqual(transaction.quantity, 5)
        self.assertEqual(transaction.responsible_user, self.admin_user)

    def test_get_transactions(self):
        # Создаём транзакцию
        Transaction.objects.create(
            transaction_type="acceptance",
            product=self.product,
            quantity=5,
            responsible_user=self.admin_user
        )
        response = self.client.get(self.transaction_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_transaction(self):
        # Создаём транзакцию
        transaction = Transaction.objects.create(
            transaction_type="acceptance",
            product=self.product,
            quantity=5,
            responsible_user=self.admin_user
        )
        url = reverse('transaction-detail', args=[transaction.id])
        data = {
            "transaction_type": "issuance",
            "product": self.product.id,
            "quantity": 3,
            "responsible_user": self.admin_user.id
        }
        response = self.client.put(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.transaction_type, "issuance")
        self.assertEqual(transaction.quantity, 3)

    def test_delete_transaction(self):
        # Создаём транзакцию
        transaction = Transaction.objects.create(
            transaction_type="acceptance",
            product=self.product,
            quantity=5,
            responsible_user=self.admin_user
        )
        url = reverse('transaction-detail', args=[transaction.id])
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)
