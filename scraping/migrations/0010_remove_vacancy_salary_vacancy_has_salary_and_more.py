# Generated by Django 4.2.3 on 2023-11-03 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0009_alter_vacancy_city_alter_vacancy_company_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='salary',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='has_salary',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='salary_max',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='salary_min',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='yearly_salary',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
