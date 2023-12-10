from django.shortcuts import render
from visualization.utils import visualize_graph, get_graph, hash_code
from django_site.forms import FindForm
import os 

def home_view(request):
    return render(request, 'home.html')

def graph_view(request):
    # if(request.GET.get('gen_graph')):
    #     visualize_graph()
    form = FindForm()
    context = {}
    context['form'] = form
    context['show'] = False

    # language = request.GET.get('language')

    language = request.GET.get('language')
    if language:
        # print(request_['language'])
        context['show'] = True
        context['path'] = os.path.join('d3graphs', f'{hash_code(language)}.html')
        # context['path'] = 'd3graph.html'
        # graph = get_graph(request_['language'])
        # visualize_graph(graph)

    return render(request, 'graph.html', context=context)