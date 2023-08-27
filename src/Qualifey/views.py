from django.shortcuts import render
from visualization.utils import visualize_graph, get_graph
from Qualifey.forms import FindForm

def home_view(request):
    return render(request, 'home.html')

def graph_view(request):
    # if(request.GET.get('gen_graph')):
    #     visualize_graph()
    form = FindForm()
    context = {}
    context['form'] = form
    context['show'] = False

    context['choices'] = form.CHOICES

    # language = request.GET.get('language')

    request_ = dict(request.GET)
    print(request.GET)
    if 'language' in request_ and request_['language']:
        print(request_['language'])
        context['show'] = True
        graph = get_graph(request_['language'])
        visualize_graph(graph)

    return render(request, 'graph.html', context=context)