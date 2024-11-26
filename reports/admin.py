from django.contrib import admin

from reports.models import DailyReport, MonthlyReport

admin.site.register(DailyReport)
admin.site.register(MonthlyReport)