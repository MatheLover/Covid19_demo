from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from .models import Covid19
@admin.register(Covid19)
class Covid19Admin(ImportExportModelAdmin):
    list_display = ('continent', 'location', 'date', 'total_cases', 'total_deaths', "reproduction_rate",
        "icu_patients", "hosp_patients",
         "total_tests", "total_vaccinations", "people_vaccinated",
         "stringency_index", "aged_65_older",
         "aged_70_older", "gdp_per_capita", "cardiovasc_death_rate",
         "diabetes_prevalence", "handwashing_facilities",
         "hospital_beds_per_thousand",
                    "Latitude", "Longitude")
