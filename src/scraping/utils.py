import os, json

current_path = os.path.join(os.getcwd(), 'scraping', 'data')
visualization_path = os.path.join(os.getcwd(), 'visualization', 'data')

def skills_connections_to_graph(input_name: str = 'skills_connections.json', output_name: str = 'global_graph.json'):
    def add_weight(source, target, weight):
        if not source in edge_weights:
            edge_weights[source] = {}
        if not target in edge_weights[source]:
            edge_weights[source][target] = 0
        edge_weights[source][target] += weight

    def add_size(node, weight):
        if not node in node_sizes:
            node_sizes[node] = 0
        node_sizes[node] += weight

    def clear_items(items):
        new_items = []
        for item in items:
            if item in subskills and subskills[item] in items:
                add_size(item, weight)
                add_weight(item, subskills[item], weight)
                add_weight(subskills[item], item, weight)
            else:
                new_items.append(item)
        return new_items

    items = read_json(os.path.join(current_path, input_name))['items']
    subskills_name = 'subskills.json'
    subskills = read_json(os.path.join(current_path, subskills_name))

    node_sizes = {}
    edge_weights = {}
    # memoization???
    for id in items.keys():
        weight = items[id]['count']

        items[id]['links'] = clear_items(items[id]['links'])

        for i, source in enumerate(items[id]['links']):
            add_size(source, weight)
            if source in subskills:
                source = subskills[source]

            for target in items[id]['links'][i+1:]:
                if target in subskills:
                    target = subskills[target]
                
                add_weight(source, target, weight)
                add_weight(target, source, weight)

    for source in edge_weights:
        for target in edge_weights[source]:
            edge_weights[source][target] /= 2

    graph = {
        'node_sizes': node_sizes,
        'edge_weights': edge_weights,
    }

    write_json(graph, os.path.join(visualization_path, 'temp.json'))

def write_json(_json, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(_json, f, indent = 4)

def read_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)