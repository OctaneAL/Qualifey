# Generated by Django 4.2.3 on 2023-09-07 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0008_alter_vacancy_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='city',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='company',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='country',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
