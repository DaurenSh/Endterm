from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Role


class UserModelTest(TestCase):
    def setUp(self):
        Role.objects.all().delete()
        self.admin_role = Role.objects.create(name="Admin", description="Administrator role")
        self.user_role = Role.objects.create(name="User", description="Regular user role")

        self.admin_user = User.objects.create_user(
            username="admin",
            password="admin123",
            role=self.admin_role
        )
        self.regular_user = User.objects.create_user(
            username="user",
            password="user123",
            role=self.user_role
        )

    def test_role_creation(self):
        self.assertEqual(Role.objects.count(), 2)
        self.assertEqual(self.admin_role.name, "Admin")
        self.assertEqual(self.user_role.name, "User")

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(self.admin_user.username, "admin")
        self.assertEqual(self.admin_user.role.name, "Admin")
        self.assertEqual(self.regular_user.role.name, "User")


class UserAPITest(APITestCase):
    def setUp(self):
        Role.objects.all().delete()
        User.objects.all().delete()

        self.user_role = Role.objects.create(name="User", description="Regular user role")

        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            role=self.user_role
        )

        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }

    def test_register_user(self):
        url = reverse('user-list')
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "role": self.user_role.id,
            "phone_number": "123456789"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, "newuser")

    def test_login_user(self):
        url = reverse('jwt-create')
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_get_user_list(self):
        url = reverse('user-list')
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
