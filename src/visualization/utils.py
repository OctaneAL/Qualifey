import os, json
import pandas as pd
from d3blocks import D3Blocks

input_path = os.path.join(os.getcwd(), 'visualization', 'data')
output_path = os.path.join(os.getcwd(), 'visualization', 'graphs')

def visualize_graph(input_name: str = 'global_graph.json', output_name: str = 'd3graph.html'):
    graph = read_json(os.path.join(input_path, input_name))
    
    source_list = []
    target_list = []
    weight_list = []
    for source in graph:
        for target in graph[source]:
            source_list.append(source)
            target_list.append(target)
            weight_list.append(graph[source][target])
        
    data = {
        'source': source_list,
        'target': target_list,
        'weight': weight_list,
    }
    
    df = pd.DataFrame(data)

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
    d3.d3graph(df, filepath='d3graph.html', charge = 200000)
    d3.D3graph.set_edge_properties(minmax_distance=[1000, 10000])
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