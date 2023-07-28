import os, json
import pandas as pd
from d3blocks import D3Blocks
from math import floor

input_path = os.path.join(os.getcwd(), 'visualization', 'data')
output_path = os.path.join(os.getcwd(), 'visualization', 'graphs')

def visualize_graph(input_name: str = 'global_graph.json', output_name: str = 'd3graph.html'):
    graph = read_json(os.path.join(input_path, input_name))
    
    k = 20
    temp = []

    source_list = []
    target_list = []
    weight_list = []
    count1 = 0
    count2 = 0
    for source in graph:
        t = 0
        count1 += 1
        for target in graph[source]:
            if graph[source][target] > 200:
                count2 += 1
                source_list.append(source)
                target_list.append(target)
                weight_list.append(graph[source][target] / k)
                t += graph[source][target] / k
            if count2 == 15:
                break
        if t != 0:
            temp.append(t)
        if count1 == 15:
            break
    temp.pop()
    sizes_ = {}
    for i in range(len(source_list)):
        if not source_list[i] in sizes_:
            sizes_[source_list[i]] = 0
        if not target_list[i] in sizes_:
            sizes_[target_list[i]] = 0
        sizes_[source_list[i]] += weight_list[i]
        sizes_[target_list[i]] += weight_list[i]
        
    data = {
        'source': source_list,
        'target': target_list,
        'weight': weight_list,
    }
    x = min(data['weight'])
    step = (max(data['weight']) - x) / 10
    max_size = 1000
    # sizes = [int(floor((weight - x) / step + 1)) for weight in temp]
    sizes = [(weight - x) / (max_size - x) * max_size for weight in temp]

    data2 = {
        'source': source_list[k:],
        'target': target_list[k:],
        'weight': weight_list[k:],
    }

    df = pd.DataFrame(data)
    df2 = pd.DataFrame(data2)

    # d3 = D3Blocks()

    # d3.elasticgraph(df, filepath = os.path.join(output_path, output_name))
    # d3.Elasticgraph.show()
    # d3.Elasticgraph.D3graph.node_properties

    #
    # Initialize
    d3 = D3Blocks()
    #
    # Import example
    # df = d3.import_example('energy') # 'bigbang', 'stormofswords'
    #
    # Create network using default

    print(sizes)
    print()
    sizes.append(5)
    print(len(sizes))
    d3.d3graph(df, filepath='d3graph.html', showfig=False, size = 5, charge = 10000)
    d3.D3graph.set_node_properties(minmax = [0, 5000])
    print(d3.D3graph.adjmat.shape[0])
    for i in d3.D3graph.node_properties:
        d3.D3graph.node_properties[i]['size'] = sizes_[i] / 50
    # d3.D3graph.node_properties['python']['size'] = 5000
    print(d3.D3graph.node_properties)
    # d3.D3graph.set_node_properties['size'] = sizes
    # d3.d3graph(df2, filepath='d3graph.html', charge = 400, showfig=False, size = 10)
    d3.D3graph.set_edge_properties(minmax_distance=[2, 1000], minmax=[0.5, 10])
    d3.D3graph.show()
    return
    # Change scaler
    d3.d3graph(df, scaler='minmax')
    #
    # Change node properties
    d3.D3graph.set_node_properties(color=None)
    d3.D3graph.node_properties['size']=30
    d3.D3graph.node_properties['color']='#FF0000'
    d3.D3graph.node_properties['edge_color']='#000000'
    d3.D3graph.node_properties['edge_size']=5
    d3.D3graph.show()
    #
    # Change edge properties
    d3.D3graph.set_edge_properties(directed=True, marker_end='arrow')
    d3.D3graph.show()
    #
    # Node properties
    d3.D3graph.node_properties
    #
    # Node properties
    d3.D3graph.edge_properties
    #
    # After making changes, show the graph again using show()
    d3.D3graph.show()

def write_json(_json, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(_json, f, indent = 4)

def read_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)