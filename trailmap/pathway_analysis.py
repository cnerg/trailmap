import networkx as nx
import matplotlib.pyplot as plt


def print_graph_parameters(G, pathways): # pragma: no cover
    '''Prints a set of parameters characterizing the graph
    '''
    print('\nGRAPH PARAMETERS')

    num_paths = get_number_of_pathways(pathways)
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

    return


def find_node_disjoint_paths(G, s, t):
    '''Returns a set of paths that share a source and target node, but have
    exactly 0 shared edges
    '''
    ndp = set()
    if s in G and t in G:
        paths = list(nx.node_disjoint_paths(G, s, t))
        [ndp.add(tuple(path)) for path in paths]
    else:
        print('source and/or target not in graph G!')

    return ndp


def find_maximum_flow(G, s, t):
    '''Finds maximum flow between a source and target node in graph G.
    Requires edge attribute 'capacity'. Any edge without 'capacity' attribute
    will be given infinite capacity and find_maximum_flow will not work as
    intended.
    '''    
    if G.is_multigraph() and G.is_directed():
        warning_message = ("Warning: Maximum flow does not support " +
        "MultiDiGraphs, the graph form that Trailmap uses. Graph will be " +
        "converted to DiGraph, which can lose information if you have " +
        "multiple edges running between two nodes. \nChecking if graph G " +
        "has an identical DiGraph representation...\n")
        print(warning_message)
        H = nx.DiGraph(G)
        
        if set(H.edges()) == set(G.edges()):
            proceed_message = ("G does not appear to have multiple edges " +
            "between any pair of nodes. No information should be lost in " +
            "the switch to DiGraph. Proceeding with flow calculation.\n")
            print(proceed_message)
        else:
            proceed_message = ("G appears to have multiple edges between at " +
            "least one pair of nodes. Information WILL be lost in the " +
            "switch to DiGraph. Proceeding with caution, consider the " +
            "results at your own risk\n")
            print(proceed_message)
        
    elif G.is_directed():
        H = G
    else:
        print("Provided graph is not a MultiDiGraph and other errors may \
            occur. Abort.\n")
        return None, None, H

    max_flow_path = nx.maximum_flow(H, s, t)
    max_flow = nx.maximum_flow_value(H, s, t)
    return max_flow_path, max_flow, H


def find_simple_cycles(G):
    '''finds cycles in a graph and returns them in a list of lists
    '''
    sc = list(nx.simple_cycles(G))
    return sc


def check_if_sublist(path, set_of_steps):
    '''Checks to see if a pathway contains each element in steps (list)
    in order. Returns True/False and the position where the cycle should be
    inserted. If False, returns -1
    '''
    pos = -1
    sub_list = False

    for i in range(len(path) - len(set_of_steps)+1):
        if path[i] == set_of_steps[0]:
            n = 1
            while (n < len(set_of_steps) and path[i+n] == set_of_steps[n]):
                n+=1
            if n == len(set_of_steps):
                sub_list = True
                pos = i + len(set_of_steps)
                break

    return sub_list, pos


def splice_cycles_into_pathways(pathways, sc):
    pathways_with_cycles = set()
    pathways = list(pathways) # turn into list, which supports indexing
    # look at all pathways and simple cycles
    for path, loop in [(x,y) for x in pathways for y in sc]:
        # check if an individual path contains an individual known loop
        (sub_list, pos) = check_if_sublist(path, loop)
        if sub_list:
            # make path into list, which is mutable
            p = list(path)
            #a dd a single loop
            p[pos:pos] = loop
            # note pathway to new list of pathways containing cycles
            pathways_with_cycles.update(p)

    return pathways_with_cycles


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


def get_number_of_pathways(pathways):
    '''returns integer number of pathways'''
    num_paths = len(pathways)

    return num_paths