import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from more_itertools import pairwise
from collections import Counter


def print_graph_parameters(G, pathways): # pragma: no cover
    '''Prints a set of parameters characterizing the graph
    '''
    print('\nGRAPH PARAMETERS')

    num_paths = len(pathways)
    print("A total of " + str(num_paths) + " pathways were generated")

    shortest = get_shortest_path(pathways)
    longest = get_longest_path(pathways)

    print("\nThe shortest pathway is length " + str(len(next(iter(shortest)))))
    print("pathways with this length are " + str(shortest))

    print("\nGraph depth is " + str(len(next(iter(longest)))))
    print("pathways with this length are " + str(longest))

    semiconnected = nx.is_semiconnected(G)
    print('\nIs the graph semiconnected? ' + str(semiconnected))
    if semiconnected is False:
        if len(list(n for n, in_deg in G.in_degree() if in_deg == 0)) > 1:
            print("You have multiple source facilities")

    hierarchy = nx.flow_hierarchy(G)
    print("\nGraph hierarchy is " + "{:.3f}".format(hierarchy))

    return


def find_node_disjoint_paths(G, s, t):
    '''Returns a set of paths that share a source and target node, but have
    exactly 0 shared edges.
    '''
    ndp = set()
    if s in G and t in G:
        paths = list(nx.node_disjoint_paths(G, s, t))
        [ndp.add(tuple(path)) for path in paths]
    else:
        raise ValueError('Source and/or target not in graph G!')

    return ndp


def is_multidigraph(G):
    return (G.is_directed() and G.is_multigraph())


def has_multiedges(G):
    '''Determines if graph G contains multiple edges between any pair of
    nodes. Returns True, False, or None if the provided graph is not a
    NetworkX Multigraph.
    '''
    if is_multidigraph(G):
        H = nx.DiGraph(G)
        return (sorted(H.edges()) != sorted(G.edges()))
    else:
        return None


def transform_to_digraph(G):
    '''Reduces multigraph to digraph and returns whether the transform is
    safe/does not lose edges (True), or if the the transform is unsafe
    and information is lost (False)
    '''
    if is_multidigraph(G):
        if has_multiedges(G) is False:
            safe = True
        else:
            safe = False
        H = nx.DiGraph(G)
        return H, safe
    elif G.is_directed():
        return G, True
    else:
        return None, False


def find_maximum_flow(H, s, t):
    '''Finds maximum flow between a source and target node in DiGraph G.
    Requires edge attribute 'capacity'. MultiDiGraphs not supported.
    '''    
    if type(H) == nx.classes.digraph.DiGraph:
        max_flow_path = nx.maximum_flow(H, s, t)
        max_flow = nx.maximum_flow_value(H, s, t)
        return max_flow_path, max_flow
    else:
        raise TypeError('Graph must be DiGraph type. Use \
            convert_to_digraph to help convert a MultiDiGraph to a DiGraph, \
            which may result in loss of information')


def find_pathway_flow(H, pathway):
    '''returns the maximum permissible flow for a given pathway in DiGraph G. 
    Any edge without 'capacity' attribute will be given infinite capacity.
    MultiDiGraphs not supported.
    '''
    if type(H) == nx.classes.digraph.DiGraph:
        edges = set(pairwise(pathway))
        H_sg = H.edge_subgraph(edges).copy()

        sources = get_sources(H_sg)
        sinks = get_sinks(H_sg)

        path_flow = nx.maximum_flow_value(H_sg, sources[0], sinks[0])
            
        return path_flow

    elif type(H) == nx.classes.multidigraph.MultiDiGraph:
        raise TypeError('Graph must be DiGraph type. Use \
            convert_to_digraph to help convert a MultiDiGraph to a DiGraph, \
            which may result in loss of information')
    else:
        raise TypeError('Graph must be DiGraph type.')


def find_simple_cycles(G): # pragma: no cover
    '''finds cycles in a graph and returns them in a list of lists.
    '''
    sc = list(nx.simple_cycles(G))
    return sc


def check_if_sublist(path, list_of_steps):
    '''Checks to see if a pathway contains each element in steps (list)
    in order. Returns the position where the steps begin. If False, returns
    position -1.
    '''
    pos = -1

    if len(path) is 0 or len(list_of_steps) is 0:
        return pos

    for i in range(len(path) - len(list_of_steps)+1):
        if path[i] == list_of_steps[0]:
            n = 1
            while (n < len(list_of_steps) and path[i+n] == list_of_steps[n]):
                n+=1
            if n == len(list_of_steps):
                pos = i
                break

    return pos


def roll_cycle(path, cycle):
    '''Checks if a cycle can be entered from a node in a simple path. If so,
    finds the last overlapping node and rolls the cycle so it begins with that
    node. Returns an empty tuple if the cycle does not overlap with the path.
    '''
    rolled = None
    # find the shared node that appears last in the path
    for node in path[-1:0:-1]:
        if node in cycle:
            rolled = tuple(np.roll(cycle, -cycle.index(node)),)
            break

    return rolled


def insert_cycles(pathway, rolled_cycles):
    '''Inserts already-rolled cycles as a tuple into a path
    '''
    path=list(pathway)
    for rc in rolled_cycles:
        path.insert(path.index(rc[0]), rc)
    path_with_cycles = tuple(path)
    return tuple(path)


def get_pathways_with_cycles(pathways, sc):
    '''For the given list of pathways and simple cycles, returns a set of
    pathways that could contain 1 or more cycles
    '''
    if len(pathways) is 0:
        return set()

    pathways_with_cycles = set()
    for path in pathways:
        rolled_cycles = set()
        for cycle in sc:
            rolled_cycle = roll_cycle(path, cycle)
            if rolled_cycle:
                rolled_cycles.add(rolled_cycle)
        
        # record all the pathways that have cycles, insert single cycle
        if rolled_cycles:
            pathways_with_cycles.add(insert_cycles(path, rolled_cycles))

    return pathways_with_cycles


def find_paths_with_source(pathways, source):
    '''returns a subset of pathways that contain a given facility as the source
    '''
    if len(pathways) is 0:
        return set()

    subset_pathways = set([ path for path in pathways if path[0] == source])
    return subset_pathways


def find_paths_with_sink(pathways, sink):
    '''returns a subset of pathways that contain a given facility as the sink
    '''
    if len(pathways) is 0:
        return set()
    
    subset_pathways = set([ path for path in pathways if path[-1] == sink])
    return subset_pathways


def find_paths_containing_all(pathways, facilities):
    '''returns a subset of pathways that contain all facilities in input list
    '''
    if len(pathways) is 0:
        return set()

    # convert to list if user passed a string or int
    if type(facilities) == int or type(facilities) == str:
        facilities = [facilities]
    
    # if user passed an empty list, return no pathways
    if not facilities:
        return set()

    p = set([path for path in pathways if set(facilities).issubset(path)])

    return p


def find_paths_containing_one_of(pathways, facilities):
    '''Returns a subset of pathways that contain one or more facilities in
    input list
    '''
    # convert to list if user passed a string or int
    if type(facilities) == int or type(facilities) == str:
        facilities = [facilities]

    # if user passed an empty list, return no pathways
    if len(pathways) is 0 or len(facilities) is 0:
        return set()

    facilities = set(facilities)
    p = set([path for path in pathways if set(path).intersection(facilities)])

    return p


def get_shortest_path(pathways):
    '''Finds the set of pathways with the shortest number of steps from source to
    target. Returns a tuple with path and length.
    '''
    #check that there are no single-item pathways
    check_for_invalid_pathways(pathways)

    if len(pathways) is not 0:
        short_len = min([len(path) for path in pathways])
        shortest = set([path for path in pathways if len(path) == short_len])
    else:
        shortest = set()

    return shortest


def get_longest_path(pathways):
    '''Finds the pathway with the longest number of steps from source to
    target. Returns a tuple with path and length.
    '''
    #check that there are no single-item pathways
    check_for_invalid_pathways(pathways)
    
    if len(pathways) is not 0:
        long_len = max([len(path) for path in pathways])
        longest = set([path for path in pathways if len(path) == long_len])
    else:
        longest = set()

    return longest


def get_sources(G):
    '''Returns nodes that have no incoming edges.
    '''
    sources = list(node for node, in_deg in G.in_degree() if in_deg == 0)
    return sources


def get_sinks(G):
    '''Returns nodes that have no outgoing edges.
    '''
    sinks = list(node for node, out_deg in G.out_degree() if out_deg == 0)
    return sinks


def sort_by_shortest(pathways):
    '''Returns the pathways sorted from shortest to longest
    '''
    #check that there are no single-item pathways
    check_for_invalid_pathways(pathways)
    return sorted(list(pathways), key=len)


def sort_by_longest(pathways):
    '''Returns the pathways sorted from shortest to longest
    '''
    #check that there are no single-item pathways
    check_for_invalid_pathways(pathways)
    return sorted(list(pathways), key=len, reverse=True)


def check_for_invalid_pathways(pathways):
    '''checks if pathways contains any errors, such as having single-value
    pathways, such as ('facility')
    '''
    if any([isinstance(i,(int,float,str)) for i in pathways]):
        raise TypeError('pathways contains pathway(s) with only one facility'\
                         ". All pathways should include at least two items")

    return