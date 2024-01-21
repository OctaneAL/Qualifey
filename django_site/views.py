from django.shortcuts import render
from visualization.utils import visualize_graph, get_graph, hash_code, get_increase_data
from scraping.models import Skill, AvailableVacancies, Country, JobTitle
from datetime import datetime
import os, json
from math import floor

def home_view(request):
    country = 'Germany'

    job_titles = [obj.name for obj in JobTitle.objects.all()]

    # lower_bound = datetime(2023, 12, 20)
    # upper_bound = datetime(2023, 12, 21)
    # countries = ["Germany", "France", "Belgium", "Netherlands"]
    # values = [
    #     AvailableVacancies.objects.get(timestamp__gt = lower_bound, timestamp__lt = upper_bound, country__name = country, jobtitle__name = job_title, source__name = 'EURES').count for country in countries
    # ]


    # data = [(obj.timestamp, obj.count) for obj in AvailableVacancies.objects.filter(country__name = country, source__name = 'EURES', jobtitle__name = job_title)]
    # data.sort(key = lambda x: x[0])

    # dates = []
    # counts = []
    # for timestamp, count in data:
    #     dates.append(timestamp.strftime('%d/%m'))
    #     counts.append(count)

    percents = {}

    for job_title in job_titles:
        a, b = get_increase_data(job_title = job_title, country = country, convert_date = False)
        
        days = [[] for _ in range(7)]

        for date, val in zip(a, b):
            days[date.weekday()].append(val)

        for i in range(7):
            days[i] = days[i][:7]
        
        days_sum = sum([sum(day) for day in days])
        
        days_percent = [round(sum(day) / days_sum * 100) for day in days]

        percents[job_title] = {
            'percents': days_percent[:],
            'days_sum': [sum(day) for day in days],
            'days': days[:],
            'max': days_sum,
        }

    xValues = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    yValues = []

    for i in range(7):
        x = 0
        for job_title in job_titles:
            x += percents[job_title]['percents'][i]
        x /= 3
        yValues.append(round(x))

    context = {
        'xValues': json.dumps(xValues),
        'yValues': json.dumps(yValues),
    }
    return render(request, 'home.html', context=context)