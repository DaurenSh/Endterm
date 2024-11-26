from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Role, User
from products.models import Category
from .models import DailyReport, MonthlyReport
from datetime import date


class ReportModelTest(TestCase):
    def setUp(self):
        Role.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

        self.admin_role = Role.objects.create(name="Admin")
        self.user = User.objects.create_user(username="admin", password="admin123", role=self.admin_role)

        self.category = Category.objects.create(name="Electronics", description="Devices and gadgets")

    def test_daily_report_creation(self):
        report = DailyReport.objects.create(
            date=date(2024, 11, 19),
            category=self.category,
            total_products_received=100,
            total_products_issued=50,
            report_generated_by=self.user
        )
        self.assertEqual(report.date, date(2024, 11, 19))
        self.assertEqual(report.category, self.category)
        self.assertEqual(report.total_products_received, 100)
        self.assertEqual(report.total_products_issued, 50)
        self.assertEqual(report.report_generated_by, self.user)

    def test_monthly_report_creation(self):
        report = MonthlyReport.objects.create(
            date=date(2024, 11, 1),
            category=self.category,
            total_products_received=500,
            total_products_issued=200,
            report_generated_by=self.user
        )
        self.assertEqual(report.date, date(2024, 11, 1))
        self.assertEqual(report.category, self.category)
        self.assertEqual(report.total_products_received, 500)
        self.assertEqual(report.total_products_issued, 200)
        self.assertEqual(report.report_generated_by, self.user)


class ReportAPITest(APITestCase):
    def setUp(self):
        Role.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

        self.admin_role = Role.objects.create(name="Admin")
        self.user = User.objects.create_user(username="admin", password="admin123", role=self.admin_role)
        self.category = Category.objects.create(name="Electronics", description="Devices and gadgets")

        response = self.client.post(reverse('jwt-create'), {'username': 'admin', 'password': 'admin123'})
        self.token = f"Bearer {response.data['access']}"
        self.auth_headers = {
            "HTTP_AUTHORIZATION": self.token
        }

        self.daily_report_url = reverse('daily-report-list')
        self.monthly_report_url = reverse('monthly-report-list')

    def test_create_daily_report(self):
        data = {
            "date": "2024-11-19",
            "category": self.category.id,
            "total_products_received": 100,
            "total_products_issued": 50,
            "report_generated_by": self.user.id
        }
        response = self.client.post(self.daily_report_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DailyReport.objects.count(), 1)
        self.assertEqual(DailyReport.objects.first().total_products_received, 100)

    def test_get_daily_reports(self):
        DailyReport.objects.create(
            date=date(2024, 11, 19),
            category=self.category,
            total_products_received=100,
            total_products_issued=50,
            report_generated_by=self.user
        )
        response = self.client.get(self.daily_report_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_daily_report(self):
        report = DailyReport.objects.create(
            date=date(2024, 11, 19),
            category=self.category,
            total_products_received=100,
            total_products_issued=50,
            report_generated_by=self.user
        )
        url = reverse('daily-report-detail', args=[report.id])
        data = {
            "date": "2024-11-19",
            "category": self.category.id,
            "total_products_received": 200,
            "total_products_issued": 100,
            "report_generated_by": self.user.id
        }
        response = self.client.put(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        report.refresh_from_db()
        self.assertEqual(report.total_products_received, 200)
        self.assertEqual(report.total_products_issued, 100)

    def test_delete_daily_report(self):
        report = DailyReport.objects.create(
            date=date(2024, 11, 19),
            category=self.category,
            total_products_received=100,
            total_products_issued=50,
            report_generated_by=self.user
        )
        url = reverse('daily-report-detail', args=[report.id])
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DailyReport.objects.count(), 0)
