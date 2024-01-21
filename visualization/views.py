from django.shortcuts import render
from visualization.utils import visualize_graph, get_graph, hash_code, get_count_data, get_increase_data
from django_site.forms import FindForm, ChartCountForm, ChartIncreaseForm
from scraping.models import Skill, AvailableVacancies, Country, JobTitle
from datetime import datetime
import os, json

def graph_view(request):
    # if(request.GET.get('gen_graph')):
    #     visualize_graph()
    language = request.GET.get('language')

    dct = {
        'language': 'Python'
    }

    if language:
        dct['language'] = language
    
    form = FindForm(initial = dct)
    context = {}
    context['form'] = form
    context['show'] = False

    # language = request.GET.get('language')

    
    if language and Skill.objects.filter(skill = language).exists():
        context['show'] = True
        # print(request_['language'])
        context['path'] = os.path.join('d3graphs', f'{hash_code(language)}.html')
        # context['path'] = 'd3graph.html'
        # graph = get_graph(request_['language'])
        # visualize_graph(graph)

    return render(request, 'graph.html', context=context)

def chart_count_view(request):
    job_title = request.GET.get('job_title')
    country = request.GET.get('country')

    dct = {
        'job_title': 'Software Developer',
        'country': 'Germany'
    }

    if job_title:
        dct['job_title'] = job_title
    if country:
        dct['country'] = country

    form = ChartCountForm(initial = dct)

    chart_id = 'count'

    context = {}
    context['chart_id'] = chart_id
    context['form'] = form
    context['label'] = None
    context['xValues'] = []
    context['data'] = []
    context['show'] = False

    if job_title and country and Country.objects.filter(name = country).exists() and JobTitle.objects.filter(name = job_title).exists():
        context['show'] = True
        context['label'] = country
        
        # scrape from all sources ???

        context['xValues'], context['data'] = get_count_data(job_title = job_title, country = country)

    return render(request, 'charts.html', context=context)

def chart_increase_view(request):
    job_title = request.GET.get('job_title')
    country = request.GET.get('country')

    dct = {
        'job_title': 'Software Developer',
        'country': 'Germany'
    }

    if job_title:
        dct['job_title'] = job_title
    if country:
        dct['country'] = country

    form = ChartIncreaseForm(initial = dct)

    chart_id = 'increase'

    context = {}
    context['chart_id'] = chart_id
    context['form'] = form
    context['label'] = None
    context['xValues'] = []
    context['data'] = []
    context['show'] = False

    if job_title and country and Country.objects.filter(name = country).exists() and JobTitle.objects.filter(name = job_title).exists():
        context['show'] = True
        context['label'] = country
        
        # scrape from all sources ???

        context['xValues'], context['data'] = get_increase_data(job_title = job_title, country = country)

    return render(request, 'charts.html', context=context)