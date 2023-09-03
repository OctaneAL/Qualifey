# Generated by Django 4.2.3 on 2023-09-03 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='company',
            field=models.CharField(max_length=128),
        ),
        migrations.CreateModel(
            name='Skill_phrase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase', models.CharField(max_length=128)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.skill')),
            ],
        ),
    ]
