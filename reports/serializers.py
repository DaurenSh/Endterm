from rest_framework import serializers
from .models import DailyReport, MonthlyReport


class DailyReportSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    report_generated_by_name = serializers.ReadOnlyField(source="report_generated_by.username")

    class Meta:
        model = DailyReport
        fields = ['id', 'date', 'category', 'category_name', 'total_products_received', 'total_products_issued', 'report_generated_by', 'report_generated_by_name']


class MonthlyReportSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    report_generated_by_name = serializers.ReadOnlyField(source="report_generated_by.username")

    class Meta:
        model = MonthlyReport
        fields = ['id', 'date', 'category', 'category_name', 'total_products_received', 'total_products_issued', 'report_generated_by', 'report_generated_by_name']
