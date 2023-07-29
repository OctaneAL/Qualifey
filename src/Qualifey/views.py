from django.shortcuts import render
from visualization.utils import visualize_graph

def home_view(request):
    return render(request, 'home.html')

def graph_view(request):
    if(request.GET.get('gen_graph')):
        visualize_graph()
    return render(request, 'd3graph.html')