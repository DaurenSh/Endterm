from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import DailyReportViewSet, MonthlyReportViewSet, daily_report_list, AnalyticsAPIView, monthly_report_list
from django.urls import path, include

router = DefaultRouter()
router.register(r'daily-reports', DailyReportViewSet, basename='daily-report')
router.register(r'monthly-reports', MonthlyReportViewSet, basename='monthly-report')

urlpatterns = [
    path('', include(router.urls)),
    path('daily-reports-list/', daily_report_list, name='daily_report_list'),
    path('monthly-reports-list/', monthly_report_list, name='monthly_report_list'),
    path('analytics/api/', AnalyticsAPIView.as_view(), name='analytics_api'),
    path('analytics/', TemplateView.as_view(template_name='reports/analytics.html'), name='analytics'),
]