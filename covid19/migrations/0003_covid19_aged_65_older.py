# Generated by Django 3.1.5 on 2021-03-17 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0002_auto_20210317_0732'),
    ]

    operations = [
        migrations.AddField(
            model_name='covid19',
            name='aged_65_older',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=13),
        ),
    ]
