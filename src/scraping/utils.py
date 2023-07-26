import os, json

current_path = os.path.join(os.getcwd(), 'scraping', 'data')
visualization_path = os.path.join(os.getcwd(), 'visualization', 'data')

def skills_connections_to_graph(input_name: str = 'skills_connections.json', output_name: str = 'global_graph.json'):
    items = read_json(os.path.join(current_path, input_name))['items']

    graph = {} # name: {name1: weight1, name2: weight2, ...}

    for id in items.keys():
        weight = items[id]['count']

        for i, source in enumerate(items[id]['links']):
            if not source in graph:
                graph[source] = {}

            for target in items[id]['links'][i+1:]:
                if not target in graph[source]:
                    graph[source][target] = weight
                else:
                    graph[source][target] += weight
                

                if not target in graph:
                    graph[target] = {}
                
                if not source in graph[target]:
                    graph[target][source] = weight
                else:
                    graph[target][source] += weight
    
    for source in graph.keys():
        for target in graph[source].keys():
            graph[source][target] /= 2
    
    write_json(graph, os.path.join(visualization_path, output_name))

def write_json(_json, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(_json, f, indent = 4)

def read_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)