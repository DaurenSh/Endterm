from django.contrib import admin

from reports.models import DailyReport, MonthlyReport

# Register your models here.
admin.site.register(DailyReport)
admin.site.register(MonthlyReport)