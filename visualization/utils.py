import os, json, hashlib
import pandas as pd
from d3blocks import D3Blocks
from math import floor
from scraping.models import Skill, Graph, AvailableVacancies, Vacancy


input_path = os.path.join(os.getcwd(), 'visualization', 'data')
output_path = os.path.join(os.getcwd(), 'templates')

def format_date(timestamp):
    return timestamp.strftime('%d/%m/%Y')

def get_count_data(job_title: str, country: str) -> tuple[list]:
    dates = []
    counts = []

    if country == 'Ukraine':
        source_name = 'djinni'
    else:
        source_name = 'EURES'

    data = [(obj.timestamp, obj.count) for obj in AvailableVacancies.objects.filter(country__name = country, source__name = source_name, jobtitle__name = job_title)]
    data.sort(key = lambda x: x[0])

    for timestamp, count in data:
        dates.append(format_date(timestamp = timestamp))
        counts.append(count)

    return (dates, counts)

def get_increase_data(job_title: str, country: str, convert_date: bool = True) -> tuple[list]:
    dates = []
    increases = []

    source_name = 'EURES'

    t = {}

    for obj in Vacancy.objects.filter(country__name = country, jobtitle__name = job_title, source__name = source_name):
        # timestamp = format_date(obj.timestamp)
        timestamp = obj.timestamp.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

        if not timestamp in t:
            t[timestamp] = 1
        else:
            t[timestamp] += 1
    
    for date, increase in sorted(zip(t.keys(), t.values()), key = lambda x: x[0]):
        if convert_date:
            dates.append(format_date(date))
        else:
            dates.append(date)
        increases.append(increase)
    
    return (dates, increases)

def visualize_global_graph(input_name: str = 'global_graph.json', output_name: str = 'd3graph.html'):
    graph = read_json(os.path.join(input_path, input_name))

    node_sizes = graph['node_sizes']
    edge_weights = graph['edge_weights']

    source_list = []
    target_list = []
    weight_list = []
    
    for source in edge_weights:
        for target in edge_weights[source]:
            if edge_weights[source][target] < 150: # Коефіцієнт
                continue
            source_list.append(source)
            target_list.append(target)
            weight_list.append(edge_weights[source][target] / 20) # Коефіцієнт

    data = {
        'source': source_list,
        'target': target_list,
        'weight': weight_list,
    }
    x = min(data['weight'])

    df = pd.DataFrame(data)

    d3 = D3Blocks()

    d3.d3graph(df, filepath=os.path.join(output_path, output_name), showfig=False, size = 5, charge = 15000)
    # d3.D3graph.set_node_properties(minmax = [0, 5000])
    d3.D3graph.set_edge_properties(minmax_distance=[200, 2000], minmax=[0.5, 10])
    # print(d3.D3graph.adjmat.shape[0])
    for i in node_sizes:
        if i in d3.D3graph.node_properties:
            d3.D3graph.node_properties[i]['size'] = node_sizes[i] / 200
            d3.D3graph.node_properties[i]['fontsize'] = max(d3.D3graph.node_properties[i]['size'] * 0.5, 4)
            d3.D3graph.node_properties[i]['fontcolor'] = '#16EE30'

    for i in d3.D3graph.edge_properties:
        if i in d3.D3graph.edge_properties:
            d3.D3graph.edge_properties[i]['weight_scaled'] /= 2

    d3.D3graph.show(filepath=os.path.join(output_path, output_name), showfig = False)
    
    divide_html_into_blocks(os.path.join(output_path, output_name))

def divide_html_into_blocks(path: str):
    def delete_title(text):
        if not ('<title>' in text and '</title>' in text):
            return text
        return text[:text.find('<title>')] + text[text.find('</title>')+8:]
    
    def get_head_block(text):
        return '{% block head %}\n' + text[text.find('<script'):text.find('</head>')] + '\n{% endblock %}'
    
    def get_body_block(text):
        text = text[text.find('<body>')+6:text.find('</body>')]
        # text = text.replace('<body>', '{% block body %}')
        # text = text.replace('</body>', '{% endblock %}')
        return text
    
    def delete_useless_scripts(text):
        return text.replace("<script async src='https://media.ethicalads.io/media/client/ethicalads.min.js'></script>", "")
    
    def change_insert_position(text):
        return text.replace('var svg = d3.select("body").append("svg")', 'var svg = d3.select("h3").append("svg")')
    
    def change_text(text):
        return text.replace('Edge Threshold', 'Edge Threshold<br>')

    # print(path)

    text = read_html(path)

    text = get_body_block(text)

    text = change_insert_position(text)

    text = change_text(text)

    # text = delete_useless_scripts(text)

    # text = delete_title(text)

    # head_block = get_head_block(text)

    # body_block = get_body_block(text)

    # text = '{% extends "home.html" %}\n' + head_block + '\n' + body_block

    write_html(path, text)

def hash_code(s: str) -> str:
    return str(hashlib.sha512(s.encode('utf-8')).hexdigest())

# Do check for keyword correctness !!!
def get_graph(keyword: str):
    # path = os.path.join(os.getcwd(), 'static', 'graphs_data', f'{hash_code(keyword)}.json')
    # graph = read_json(path)

    graph = Graph.objects.get(skill_id = Skill.objects.get(skill = keyword).id).data
    
    if not keyword in graph['edge_weights']: # graph is empty
        return None

    graph_dict = {} # (source, target): weight
                    # !!! source lexicographically smaller than target

    source_list = []
    target_list = []
    weight_list = []
    nodes = {}

    nodes_list = set(graph['edge_weights'][keyword])
    nodes_list.add(keyword)
    
    for source_ in list(nodes_list):
        nodes[source_] = graph['node_sizes'][source_]
        for target in graph['edge_weights'][source_]:
            nodes[target] = graph['node_sizes'][target]

            source = source_

            if source > target:
                source, target = target, source
            
            graph_dict[(source, target)] = graph['edge_weights'][source][target]
    
    for pair in graph_dict:
        source_list.append(pair[0])
        target_list.append(pair[1])
        weight_list.append(graph_dict[pair])

    edges = {
        'source': source_list,
        'target': target_list,
        'weight': weight_list,
    }

    res = {
        'edges': edges,
        'nodes': nodes,
    }

    return res

def visualize_graph(keyword: str):
    def filter_edges(edges, k):
        length = len(edges['source'])

        count = 0
        if length <= 10:
            count = length
        else:
            count = max(10, length // 50)

        edges['source'] = edges['source'][:count]
        edges['target'] = edges['target'][:count]
        edges['weight'] = edges['weight'][:count]

        return edges
    
    def sort_edges(edges):
        new = [(edges['source'][i], edges['target'][i], edges['weight'][i]) for i in range(len(edges['source']))]
        new = sorted(new, key = lambda x: x[2], reverse = True)

        return {
            'source': [i[0] for i in new],
            'target': [i[1] for i in new],
            'weight': [i[2] for i in new],
        }

    output_path = os.path.join(os.getcwd(), 'templates', 'd3graphs', f'{hash_code(keyword)}.html')

    graph = get_graph(keyword=keyword)

    if graph == None:
        write_html(output_path, 'no data :(')
        return

    graph['edges'] = sort_edges(graph['edges'])


    # !!!
    # k1 - coefficient for edges (1/k1 edges will be visualizated)
    # k2 - coefficient for nodes (all sizes will be multiplied by k2)
    # !!!

    k1 = 50
    k2 = 130 / max(graph['nodes'].values())

    graph['edges'] = filter_edges(graph['edges'], k1)

    df = pd.DataFrame(graph['edges'])

    d3 = D3Blocks()
    
    d3.d3graph(df, filepath=output_path, showfig = False, charge = 7000)
    d3.D3graph.set_edge_properties(minmax_distance=[50, 5000], minmax=[0.5, 10])

    for i in graph['nodes']:
        if i in d3.D3graph.node_properties:
            d3.D3graph.node_properties[i]['size'] = graph['nodes'][i] * k2
            d3.D3graph.node_properties[i]['fontsize'] = max(d3.D3graph.node_properties[i]['size'] * 0.5, 4)
            d3.D3graph.node_properties[i]['fontcolor'] = '#16EE30'
    
    for i in d3.D3graph.edge_properties:
        if i in d3.D3graph.edge_properties:
            d3.D3graph.edge_properties[i]['weight_scaled'] /= 2

    d3.D3graph.show(filepath=output_path, showfig = False)

    divide_html_into_blocks(path = output_path)

def write_json(_json, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(_json, f, indent = 4)

def read_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_html(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return ''.join(f.readlines())

def write_html(path: str, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)