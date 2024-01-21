from datetime import datetime
from scraping.models import Vacancy, Country, JobTitle, AvailableVacancies
import matplotlib.pyplot as plt

def add_increase_plot(jobtitle, country):
    x = []
    y = []

    for a, b in sorted(zip(list(da[jobtitle][country].keys()), list(da[jobtitle][country].values())), key = lambda x: x[0]):
        x.append(a)
        y.append(b)
    
    plt.plot(x, y)

def add_increase_plot_all(jobtitle):
    x = []
    y = []

    data = {}
    for country in da[jobtitle]:
        for date in list(da[jobtitle][country].keys()):
            if not date in data:
                data[date] = da[jobtitle][country][date]
            else:
                data[date] += da[jobtitle][country][date]

    for a, b in sorted(zip(list(data.keys()), list(data.values())), key = lambda x: x[0]):
        x.append(a)
        y.append(b)
    
    plt.plot(x, y)

def add_count_plot(jobtitle, country):
    x = []
    y = []

    for a, b in sorted([(obj.timestamp, obj.count) for obj in AvailableVacancies.objects.filter(country_id = Country.objects.get(abbreviation = country).id, jobtitle_id = JobTitle.objects.get(name = jobtitle))], key = lambda x: x[0]):
        x.append(a.replace(hour = 0, minute = 0, second = 0, microsecond = 0))
        y.append(b)

    plt.plot(x, y)

def add_count_plot_all(jobtitle):
    x = []
    y = []

    data = {}
    for obj in AvailableVacancies.objects.filter(jobtitle_id = JobTitle.objects.get(name = jobtitle)):
        date = obj.timestamp.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        if not date in data:
            data[date] = obj.count
        else:
            data[date] += obj.count

    for a, b in sorted(zip(list(data.keys()), list(data.values()))):
        x.append(a)
        y.append(b)
    
    plt.plot(x, y)

def save_plot():
    plt.savefig('/var/www/dima/data/www/qualifey.com/django-apps/django_site/visualization/lol.png')

def clear_plot():
    plt.cla()

def get_data():
    for obj in JobTitle.objects.all():
        me_jo[obj.id] = obj.name
    for obj in Country.objects.all():
        me_co[obj.id] = obj.abbreviation

    for jobtitle in JobTitle.objects.all():
        da[me_jo[jobtitle.id]] = {}
        for country in Country.objects.all():
            da[me_jo[jobtitle.id]][me_co[country.id]] = {}

    for obj in Vacancy.objects.all():
        jobtitle = me_jo[obj.jobtitle_id]
        country = me_co[obj.country_id]
        date = obj.timestamp
        date = date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        if da[jobtitle][country] == []:
            da[jobtitle][country] = {}
        if not date in da[jobtitle][country]:
            da[jobtitle][country][date] = 1
        else:
            da[jobtitle][country][date] += 1

me_jo = {}
me_co = {}
da = {}

get_data()