import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from more_itertools import pairwise
from collections import Counter
import math


def print_graph_parameters(G, pathways): # pragma: no cover
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
        print('source and/or target not in graph G!')

    return ndp


def has_multiedges(G):
    '''Determines if graph G contains multiple edges between any pair of
    nodes. Returns 0 if False, 1 if True, and -1 if the provided graph is not
    a NetworkX Multigraph.
    '''
    if G.is_multigraph():
        H = nx.DiGraph(G)
        if sorted(H.edges()) == sorted(G.edges()):
            multiedges = False
        else:
            multiedges = True
    else:
        multiedges = None

    return multiedges


def find_maximum_flow(G, s, t):
    '''Finds maximum flow between a source and target node in graph G.
    Requires edge attribute 'capacity'. Any edge without 'capacity' attribute
    will be given infinite capacity and find_maximum_flow will not work as
    intended.
    '''    

    warning_message = ("Warning: Maximum flow does not support " +
        "MultiDiGraphs, the graph form that Trailmap uses. Graph will be " +
        "converted to DiGraph, which can lose information if you have " +
        "multiple edges running between two nodes. \nChecking if graph G " +
        "has an identical DiGraph representation...\n")

    if G.is_directed():
        multiedges = has_multiedges(G)
        if multiedges == True:
            print(warning_message)
            print("G appears to have multiple edges between at least one " +
            "pair of nodes. Information WILL be lost in the switch to " +
            "DiGraph. Proceeding with caution, consider the results at " +
            "your own risk\n")
            H = nx.DiGraph(G)
        elif multiedges == False:
            print(warning_message)
            print("G does not appear to have multiple edges between any " +
            "pair of nodes. No information should be lost in the switch to " +
            "DiGraph. Proceeding with flow calculation.\n")
            H = nx.DiGraph(G)
        else:
            H=G
    else:
        print("Provided graph is not a MultiDiGraph or DiGraph and other \
        errors may occur. Abort.\n")
        return None, None, G

    max_flow_path = nx.maximum_flow(H, s, t)
    max_flow = nx.maximum_flow_value(H, s, t)
    return max_flow_path, max_flow, H


def find_pathway_flow(G, pathway):
    '''returns the maximum permissible flow for a given pathway. Any edge
    without 'capacity' attribute will be given infinite capacity.
    '''
    multiedges = has_multiedges(G)
    if multiedges != True:
        # graph either has no multiedges, or is not in MultiDiGraph format
        H = nx.DiGraph(G)
        edges = set(pairwise(pathway))
        H_sg = H.edge_subgraph(edges).copy()

        sources = get_sources(H_sg)
        sinks = get_sinks(H_sg)


        path_flow = nx.maximum_flow_value(H_sg, sources[0], sinks[0])
            
        return path_flow

    else:
        print("Provided pathway has multiple edges. Flow calculation across \
               multi-edged pathways is currently unsupported. Returning None")
        return None


def find_simple_cycles(G): # pragma: no cover
    '''finds cycles in a graph and returns them in a list of lists.
    '''
    sc = list(nx.simple_cycles(G))
    return sc


def check_if_sublist(path, list_of_steps):
    '''Checks to see if a pathway contains each element in steps (list)
    in order. Returns True/False and the position where the steps begin. If
    False, returns position -1.
    '''
    pos = -1
    sub_list = False

    for i in range(len(path) - len(list_of_steps)+1):
        if path[i] == list_of_steps[0]:
            n = 1
            while (n < len(list_of_steps) and path[i+n] == list_of_steps[n]):
                n+=1
            if n == len(list_of_steps):
                sub_list = True
                pos = i
                break

    return sub_list, pos


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
    subset_pathways = set([ path for path in pathways if path[0] == source])
    return subset_pathways


def find_paths_with_sink(pathways, sink):
    '''returns a subset of pathways that contain a given facility as the sink
    '''
    subset_pathways = set([ path for path in pathways if path[-1] == sink])
    return subset_pathways


def find_paths_containing_all(pathways, facilities):
    '''returns a subset of pathways that contain all facilities in input list
    '''
    # convert to list if user passed a string or int
    if type(facilities) == int or type(facilities) == str:
        facilities = [facilities]
    
    # if user passed an empty list, return no pathways
    if not facilities:
        return set()

    p = set()
    for path in pathways:
        if set(facilities).issubset(path):
            p.add(path)

    return p


def find_paths_containing_one_of(pathways, facilities):
    '''Returns a subset of pathways that contain one or more facilities in
    input list
    '''
    # convert to list if user passed a string or int
    if type(facilities) == int or type(facilities) == str:
        facilities = [facilities]
    
    # if user passed an empty list, return no pathways
    if not facilities:
        return set()

    p = set()
    for path in pathways:
        contains = [path for facility in facilities if facility in path]
        if contains:
            p.add(contains[0])

    return p


def get_shortest_path(pathways):
    '''Finds the set of pathways with the shortest number of steps from source to
    target. Returns a tuple with path and length.
    '''
    if len(pathways) is not 0:
        shortest_length = min([len(path) for path in pathways])
        shortest = set([path for path in pathways if len(path) == shortest_length])
    else:
        shortest = set()
        shortest_length = 0

    return shortest_length, shortest


def get_longest_path(pathways):
    '''Finds the pathway with the longest number of steps from source to
    target. Returns a tuple with path and length.
    '''
    if len(pathways) is not 0:
        longest_length = max([len(path) for path in pathways])
        longest = set([path for path in pathways if len(path) == longest_length])
    else:
        longest = set()
        longest_length = 0

    return longest_length, longest


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
