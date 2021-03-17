# Generated by Django 3.1.5 on 2021-03-17 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0003_covid19_aged_65_older'),
    ]

    operations = [
        migrations.AlterField(
            model_name='covid19',
            name='gdp_per_capita',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=13),
        ),
    ]
