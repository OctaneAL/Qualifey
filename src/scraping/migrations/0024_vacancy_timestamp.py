# Generated by Django 4.2.3 on 2023-11-28 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0023_continent'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='timestamp',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]