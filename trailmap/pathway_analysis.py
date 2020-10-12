import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint


def draw_graph(G):
    pos = nx.drawing.nx_pydot.graphviz_layout(G, prog=dot)

    plt.figure()
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos)

    return


def draw_path(G, path):
    draw_graph(G)
    pos = nx.drawing.nx_pydot.graphviz_layout(G)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=path, node_color="red")
    plt.show()
    return


def print_graph_parameters(G, pathways):
    '''Prints a set of parameters characterizing the graph
    '''
    print('\nGRAPH PARAMETERS')

    num_paths = len(pathways)
    print("A total of " + str(num_paths) + " pathways were generated")

    (shortest_length, shortest) = get_shortest_path(pathways)
    (longest_length, longest) = get_longest_path(pathways)

    print("\nThe shortest pathway is length " + str(shortest_length))
    print("pathways with this length are " + str(shortest))

    print("\nGraph depth is " + str(longest_length))
    print("pathways with this length are " + str(longest))

    semiconnected = nx.is_semiconnected(G)
    print('\nIs the graph semiconnected? ' + str(semiconnected))
    if semiconnected is False:
        print("-->This is likely because you have multiple source facilities")

    hierarchy = nx.flow_hierarchy(G)
    print("\nGraph hierarchy is " + "{:.3f}".format(hierarchy))

    return num_paths, semiconnected, hierarchy


def find_node_disjoint_paths(G, s, t):
    ndp = set()
    if s in G and t in G:
        paths = list(nx.node_disjoint_paths(G, s, t))
        [ndp.add(tuple(path)) for path in paths]

    return ndp


def find_maximum_flow(G, s, t):
    '''Requires edge attribute 'capacity'
    '''
    max_flow_path = nx.maximum_flow(G, s, t)
    max_flow = nx.maximum_flow_value(G, s, t)
    return max_flow_path, max_flow


def find_simple_cycles(G):
    sc = list(nx.simple_cycles(G))
    return sc


def find_paths_with_source(pathways, source):
    '''returns a subset of pathways that contain a given facility as the source
    '''
    subset_pathways = set()
    for path in pathways:
        if path[0] == source:
            subset_pathways.add(path)

    return subset_pathways


def find_paths_with_sink(pathways, sink):
    '''returns a subset of pathways that contain a given facility as the sink
    '''
    subset_pathways = set()
    for path in pathways:
        if path[-1] == sink:
            subset_pathways.add(path)

    return subset_pathways


def find_paths_containing_all(pathways, facilities):
    '''returns a subset of pathways that contain all facilities in input list
    '''
    p = set()
    for path in pathways:
        if set(facilities).issubset(path):
            p.add(path)

    return p


def find_paths_containing_one_of(pathways, facilities):
    '''returns a subset of pathways that contain one or more facilities in
    input list
    '''
    p = set()
    for path in pathways:
        p.add([path for facility in facilities if facility in path])

    return p


def get_shortest_path(pathways):
    '''finds the pathway with the shortest number of steps from source to
    target. Returns a tuple with path and length.
    '''
    if len(pathways) is not 0:
        shortest_length = min([len(path) for path in pathways])
        shortest = [path for path in pathways if len(path) == shortest_length]
    else:
        shortest = "No pathways found"
        shortest_length = 0

    return shortest_length, shortest


def get_longest_path(pathways):
    '''finds the pathway with the longest number of steps from source to
    target. Returns a tuple with path and length.
    '''
    if len(pathways) is not 0:
        longest_length = max([len(path) for path in pathways])
        longest = [path for path in pathways if len(path) == longest_length]
    else:
        longest = "No pathways found"
        longest_length = 0

    return longest_length, longest
