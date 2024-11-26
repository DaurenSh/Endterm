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
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

class DailyReportViewSet(ModelViewSet):
    queryset = DailyReport.objects.all().order_by('-date')
    serializer_class = DailyReportSerializer

    def perform_create(self, serializer):
        logger.info(f"Creating Daily Report for category {serializer.validated_data['category']}")
        super().perform_create(serializer)
        new_report = serializer.instance
        cache_key = f"daily_report_{new_report.id}"
        cache.set(cache_key, DailyReportSerializer(new_report).data, timeout=600)
        logger.info(f"Daily Report with id {new_report.id} cached.")

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f"daily_report_{pk}"
        cached_report = cache.get(cache_key)

        if cached_report:
            return Response(cached_report, status=status.HTTP_200_OK)

        try:
            report = DailyReport.objects.get(pk=pk)
            serializer = DailyReportSerializer(report)
            cache.set(cache_key, serializer.data, timeout=600)
            logger.info(f"Daily Report with id {pk} cached.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DailyReport.DoesNotExist:
            return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        updated_report = self.get_object()
        cache_key = f"daily_report_{updated_report.id}"
        cache.set(cache_key, DailyReportSerializer(updated_report).data, timeout=600)
        logger.info(f"Daily Report with id {updated_report.id} updated in cache.")
        return response

    def destroy(self, request, *args, **kwargs):
        report = self.get_object()
        report.delete()
        cache_key = f"daily_report_{report.id}"
        cache.delete(cache_key)
        logger.info(f"Daily Report with id {report.id} removed from cache.")
        return Response(status=status.HTTP_204_NO_CONTENT)


class MonthlyReportViewSet(ModelViewSet):
    queryset = MonthlyReport.objects.all().order_by('-date')
    serializer_class = MonthlyReportSerializer

    def perform_create(self, serializer):
        logger.info(f"Creating Monthly Report for category {serializer.validated_data['category']}")
        super().perform_create(serializer)
        new_report = serializer.instance
        cache_key = f"monthly_report_{new_report.id}"
        cache.set(cache_key, MonthlyReportSerializer(new_report).data, timeout=600)
        logger.info(f"Monthly Report with id {new_report.id} cached.")

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f"monthly_report_{pk}"
        cached_report = cache.get(cache_key)

        if cached_report:
            return Response(cached_report, status=status.HTTP_200_OK)

        try:
            report = MonthlyReport.objects.get(pk=pk)
            serializer = MonthlyReportSerializer(report)
            cache.set(cache_key, serializer.data, timeout=600)
            logger.info(f"Monthly Report with id {pk} cached.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MonthlyReport.DoesNotExist:
            return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        updated_report = self.get_object()
        cache_key = f"monthly_report_{updated_report.id}"
        cache.set(cache_key, MonthlyReportSerializer(updated_report).data, timeout=600)
        logger.info(f"Monthly Report with id {updated_report.id} updated in cache.")
        return response

    def destroy(self, request, *args, **kwargs):
        report = self.get_object()
        report.delete()
        cache_key = f"monthly_report_{report.id}"
        cache.delete(cache_key)
        logger.info(f"Monthly Report with id {report.id} removed from cache.")
        return Response(status=status.HTTP_204_NO_CONTENT)

def daily_report_list(request):
    cache_key = "daily_reports_list"
    cached_reports = cache.get(cache_key)

    if cached_reports:
        logger.info(f"Returning daily reports from cache for user {request.user}")
        return render(request, 'reports/daily_report_list.html', {'reports': cached_reports})

    reports = DailyReport.objects.select_related('category', 'report_generated_by').order_by('-date')
    logger.info(f"Daily report list accessed by {request.user}")

    serializer = DailyReportSerializer(reports, many=True)
    serialized_data = serializer.data

    cache.set(cache_key, serialized_data, timeout=600)

    return render(request, 'reports/daily_report_list.html', {'reports': serialized_data})

def monthly_report_list(request):
    cache_key = "monthly_reports_list"
    cached_reports = cache.get(cache_key)

    if cached_reports:
        logger.info(f"Returning monthly reports from cache for user {request.user}")
        return render(request, 'reports/monthly_report_list.html', {'reports': cached_reports})

    reports = MonthlyReport.objects.select_related('category', 'report_generated_by').order_by('-date')
    logger.info(f"Monthly report list accessed by {request.user}")

    serializer = MonthlyReportSerializer(reports, many=True)
    serialized_data = serializer.data

    cache.set(cache_key, serialized_data, timeout=600)

    return render(request, 'reports/monthly_report_list.html', {'reports': serialized_data})

class AnalyticsAPIView(APIView):

    def get(self, request):
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        daily_reports = DailyReport.objects.filter(date__range=[start_date, end_date]) \
            .values('date') \
            .annotate(
                total_received=Sum('total_products_received'),
                total_issued=Sum('total_products_issued')
            ).order_by('date')

        data = {
            "labels": [report['date'].strftime('%Y-%m-%d') for report in daily_reports],
            "received": [report['total_received'] for report in daily_reports],
            "issued": [report['total_issued'] for report in daily_reports],
        }

        return Response(data)