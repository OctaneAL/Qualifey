# Generated by Django 4.0.5 on 2023-11-27 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0019_jobtitle_remove_country_gdp_usd_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OccuppationUri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=128)),
                ('jobtitle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.jobtitle')),
            ],
        ),
    ]
