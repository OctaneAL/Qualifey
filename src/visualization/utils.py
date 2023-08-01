import os, json
import pandas as pd
from d3blocks import D3Blocks
from math import floor

input_path = os.path.join(os.getcwd(), 'visualization', 'data')
output_path = os.path.join(os.getcwd(), 'templates')

def visualize_graph(input_name: str = 'global_graph.json', output_name: str = 'd3graph.html'):
    graph = read_json(os.path.join(input_path, input_name))
    
    k = 20
    temp = []

    source_list = []
    target_list = []
    weight_list = []
    count1 = 0
    count2 = 0
    sizes_ = {}
    for source in graph:
        t = 0
        count1 += 1
        for target in graph[source]:
            if not target in sizes_:
                sizes_[target] = 0
            if not source in sizes_:
                sizes_[source] = 0
            sizes_[target] += graph[source][target]
            sizes_[source] += graph[source][target]
            if graph[source][target] > 200:
                count2 += 1
                source_list.append(source)
                target_list.append(target)
                weight_list.append(graph[source][target] / k)
                t += graph[source][target] / k
            if count2 == 50:
                break
        if t != 0:
            temp.append(t)
        if count1 == 50:
            break
    temp.pop()
    # for i in range(len(source_list)):
    #     if not source_list[i] in sizes_:
    #         sizes_[source_list[i]] = 0
    #     if not target_list[i] in sizes_:
    #         sizes_[target_list[i]] = 0
    #     sizes_[source_list[i]] += weight_list[i]
    #     sizes_[target_list[i]] += weight_list[i]
        
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
    for i in d3.D3graph.node_properties:
        if i in d3.D3graph.node_properties:
            d3.D3graph.node_properties[i]['size'] = sizes_[i] / 2000
            d3.D3graph.node_properties[i]['fontsize'] = max(d3.D3graph.node_properties[i]['size'] * 0.5, 4)
            d3.D3graph.node_properties[i]['fontcolor'] = '#16EE30'

    for i in d3.D3graph.edge_properties:
        if i in d3.D3graph.edge_properties:
            d3.D3graph.edge_properties[i]['weight_scaled'] /= 2

    # print(d3.D3graph.node_properties)
    # print(d3.D3graph.edge_properties)
    # d3.D3graph.set_node_properties['size'] = sizes
    # d3.d3graph(df2, filepath='d3graph.html', charge = 400, showfig=False, size = 10)
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
        text = text[text.find('<body>'):text.find('</html>')]
        text = text.replace('<body>', '{% block body %}')
        text = text.replace('</body>', '{% endblock %}')
        return text
    
    def delete_useless_scripts(text):
        return text.replace("<script async src='https://media.ethicalads.io/media/client/ethicalads.min.js'></script>", "")

    print(path)

    text = read_html(path)

    text = delete_useless_scripts(text)

    text = delete_title(text)

    head_block = get_head_block(text)

    body_block = get_body_block(text)

    text = '{% extends "home.html" %}\n' + head_block + '\n' + body_block

    write_html(path, text)

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