from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from .models import Covid19
@admin.register(Covid19)
class Covid19Admin(ImportExportModelAdmin):
    list_display = ('continent', 'location', 'date', 'total_cases', 'total_deaths')
