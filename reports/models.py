from django.db import models
from products.models import Category
from django.conf import settings


class DailyReport(models.Model):
    date = models.DateField(verbose_name="Report Date")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="daily_reports")
    total_products_received = models.PositiveIntegerField(default=0, verbose_name="Total Products Received")
    total_products_issued = models.PositiveIntegerField(default=0, verbose_name="Total Products Issued")
    report_generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_reports")

    def __str__(self):
        return f"Daily Report: {self.date} - {self.category.name}"


class MonthlyReport(models.Model):
    date = models.DateField(verbose_name="Report Month")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="monthly_reports")
    total_products_received = models.PositiveIntegerField(default=0, verbose_name="Total Products Received")
    total_products_issued = models.PositiveIntegerField(default=0, verbose_name="Total Products Issued")
    report_generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="monthly_reports")

    def __str__(self):
        return f"Monthly Report: {self.date.strftime('%Y-%m')} - {self.category.name}"
