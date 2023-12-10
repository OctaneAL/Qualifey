# Generated by Django 4.0.5 on 2023-11-17 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0016_city_population'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='gdp_usd',
            field=models.BigIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='country',
            name='population',
            field=models.BigIntegerField(blank=True, default=0),
        ),
    ]