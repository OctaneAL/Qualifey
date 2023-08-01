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

    graph = {} # name: {name1: weight1, name2: weight2, ...}
    node_sizes = {}
    edge_weights = {}
    # memoization???
    for id in items.keys():
        weight = items[id]['count']

        items[id]['links'] = clear_items(items[id]['links'])

        for i, source in enumerate(items[id]['links']):
            # if source in subskills:
            #     source_main_skill = subskills[source]
            #     add_weight(source_main_skill, source, weight)
            #     add_weight(source, source_main_skill, weight)
            #     source = source_main_skill

            add_size(source, weight)
            if source in subskills:
                # add_weight(source, subskills[source], weight)
                # add_weight(subskills[source], source, weight)
                source = subskills[source]
                # add_size(source, weight)

            for target in items[id]['links'][i+1:]:
                if target in subskills:
                    # add_weight(target, subskills[target], weight)
                    # add_weight(subskills[target], target, weight)
                    target = subskills[target]
                    # add_size(target, weight)
                
                add_weight(source, target, weight)
                add_weight(target, source, weight)


                # t_source = source
                # if source in subskills:
                #     source_main_skill = subskills[source]
                #     add_weight(source_main_skill, source, weight)
                #     add_weight(source, source_main_skill, weight)
                #     t_source = source_main_skill
                # if target in subskills:
                #     target_main_skill = subskills[target]
                #     add_weight(target_main_skill, target, weight)
                #     add_weight(target, target_main_skill, weight)
                #     target = subskills[target]
                
                # add_weight(t_source, target, weight)
                # add_weight(target, t_source, weight)



                # if not target in graph[source]:
                #     graph[source][target] = weight
                # else:
                #     graph[source][target] += weight
                

                # if target in subskills:
                #     target = subskills[target]
                # if not target in graph:
                #     graph[target] = {}
                
                # if not source in graph[target]:
                #     graph[target][source] = weight
                # else:
                #     graph[target][source] += weight
    
    # DECREASE EDGES SIZES BY 2 TIMES
    for source in edge_weights:
        for target in edge_weights[source]:
            edge_weights[source][target] /= 2

    graph = {
        'node_sizes': node_sizes,
        'edge_weights': edge_weights,
    }

    write_json(graph, os.path.join(visualization_path, 'temp.json'))

    # for source in graph.keys():
    #     for target in graph[source].keys():
    #         graph[source][target] /= 2
    
    # write_json(graph, os.path.join(visualization_path, output_name))

def write_json(_json, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(_json, f, indent = 4)

def read_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)