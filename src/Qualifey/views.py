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

    language = request.GET.get('language')
    if language:
        context['show'] = True
        print(language)
        graph = get_graph(language)
        visualize_graph(graph)

    return render(request, 'graph.html', context=context)