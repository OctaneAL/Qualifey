# Generated by Django 4.0.5 on 2023-11-28 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0021_rename_occuppationuri_occupationuri'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('link', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='AvailableVacancies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.BigIntegerField()),
                ('timestamp', models.DateTimeField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.country')),
                ('jobtitle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.jobtitle')),
            ],
        ),
        migrations.AddField(
            model_name='vacancy',
            name='source',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.source'),
        ),
    ]
