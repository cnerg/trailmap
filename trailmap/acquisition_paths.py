import networkx as nx
from pprint import pprint


def conduct_apa(facility_dict_in, facility_dict_out):
    ''' '''
    G = build_graph(facility_dict_in, facility_dict_out)

    sources = list(node for node, in_deg in G.in_degree() if in_deg == 0)
    sinks = list(node for node, out_deg in G.out_degree() if out_deg == 0)

    pathways = find_simple_paths(G, sources, sinks)

    return G, pathways


def build_graph(facility_dict_in, facility_dict_out):
    '''Builds NetworkX graph from Cyclus input file
    '''
    G = nx.MultiDiGraph()
    G.add_nodes_from(facility_dict_in.keys())
    for receiver, incommods in facility_dict_in.items():
        # find all facilities with that commod as an outcommod
        for sender, outcommods in facility_dict_out.items():
            for commod in set(incommods).intersection(outcommods):
                G.add_edge(sender, receiver, commodity=commod)
    return G


def find_simple_paths(G, sources, sinks):
    ''' finds all simple paths between a given list of sources and targets
    '''
    # turn sources/sinks into list if a single string/int was submitted
    if type(sources) == int or type(sources) == str:
        sources = [sources]
    if type(sinks) == int or type(sinks) == str:
        sinks = [sinks]

    pathways = set()
    for source, sink in [(x, y) for x in sources for y in sinks]:
        pathways.update({tuple(path) for path in nx.all_simple_paths(
            G, source=source, target=sink)})

    return pathways


def print_acquisition_paths(pathways):
    print("\nSimple paths")
    pprint(pathways)

    return
