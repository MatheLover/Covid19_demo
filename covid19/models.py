from django.db import models


# Create your models here.
class Covid19(models.Model):
    continent = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    date = models.DateField()

    # Case Stat
    total_cases = models.IntegerField()
    total_deaths = models.IntegerField()
    reproduction_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    icu_patients = models.IntegerField(default=0)
    hosp_patients = models.IntegerField(default=0)


    # Public Health Response stat
    total_tests = models.IntegerField(default=0)
    total_vaccinations = models.IntegerField(default=0)
    people_vaccinated = models.IntegerField(default=0)


    # Socio-economic stat
    stringency_index = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    aged_65_older = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    aged_70_older = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    gdp_per_capita = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)


    # Public Health Stat
    cardiovasc_death_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    diabetes_prevalence = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)



    # Public Health Facility
    handwashing_facilities = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    hospital_beds_per_thousand = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    # Coordinates
    Latitude = models.DecimalField(max_digits=13, decimal_places=10, default=0.0)
    Longitude = models.DecimalField(max_digits=13, decimal_places=10, default=0.0)

