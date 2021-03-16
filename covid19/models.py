from django.db import models


# Create your models here.
class Covid19(models.Model):
    continent = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    date = models.DateField()
    total_cases = models.IntegerField()
    total_deaths = models.IntegerField()
