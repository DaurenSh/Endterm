import logging
from datetime import date, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import DailyReport, MonthlyReport
from .serializers import DailyReportSerializer, MonthlyReportSerializer
from transactions.models import Transaction
from django.db.models import Sum
from django.shortcuts import render

logger = logging.getLogger(__name__)

class DailyReportViewSet(ModelViewSet):
    queryset = DailyReport.objects.all().order_by('-date')
    serializer_class = DailyReportSerializer

    def perform_create(self, serializer):
        logger.info(f"Creating Daily Report for category {serializer.validated_data['category']}")
        super().perform_create(serializer)


class MonthlyReportViewSet(ModelViewSet):
    queryset = MonthlyReport.objects.all().order_by('-date')
    serializer_class = MonthlyReportSerializer

    def perform_create(self, serializer):
        logger.info(f"Creating Monthly Report for category {serializer.validated_data['category']}")
        super().perform_create(serializer)

def daily_report_list(request):
    reports = DailyReport.objects.select_related('category', 'report_generated_by').order_by('-date')
    logger.info(f"Daily report list accessed by {request.user}")
    return render(request, 'reports/daily_report_list.html', {'reports': reports})

def monthly_report_list(request):
    reports = MonthlyReport.objects.select_related('category', 'report_generated_by').order_by('-date')
    logger.info(f"Monthly report list accessed by {request.user}")
    return render(request, 'reports/monthly_report_list.html', {'reports': reports})

class AnalyticsAPIView(APIView):

    def get(self, request):
        # Получаем данные за последние 30 дней
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        # Агрегация данных
        daily_reports = DailyReport.objects.filter(date__range=[start_date, end_date]) \
            .values('date') \
            .annotate(
                total_received=Sum('total_products_received'),
                total_issued=Sum('total_products_issued')
            ).order_by('date')

        # Форматируем данные для графика
        data = {
            "labels": [report['date'].strftime('%Y-%m-%d') for report in daily_reports],
            "received": [report['total_received'] for report in daily_reports],
            "issued": [report['total_issued'] for report in daily_reports],
        }

        return Response(data)