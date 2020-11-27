import trailmap.acquisition_paths as ap
import trailmap.parse_input as pi
import networkx as nx
import pytest
from tests.ap_data import testdata
# testdata format
# name, edges, facility_dict_in, facility_dict_out, exp_paths


@pytest.mark.parametrize("name, edges, fd_in, fd_out, exp_paths", testdata)
def test_build_graph(name, edges, fd_in, fd_out, exp_paths):
    exp_G = nx.MultiDiGraph()
    exp_G.add_edges_from(edges)
    obs_G = ap.build_graph(fd_in, fd_out)

    assert nx.graph_edit_distance(exp_G, obs_G) == 0


@pytest.mark.parametrize("name, edges, fd_in, fd_out, exp_paths", testdata)
def test_find_simple_paths(name, edges, fd_in, fd_out, exp_paths):
    G = nx.MultiDiGraph()
    G.add_edges_from(edges)

    sources = []
    sinks = []
    for node, degree in G.in_degree():
        if degree == 0:
            sources.append(node)
    for node, degree in G.out_degree():
        if degree == 0:
            sinks.append(node)

    obs_pathways = ap.find_simple_paths(G, sources, sinks)

    assert exp_paths == obs_pathways


def test_find_simple_paths_str_sources():
    G = nx.MultiDiGraph()
    edges = [("A","B"), ("B","C")]
    G.add_edges_from(edges)
    sources = "A"
    sinks = ["C"]
    exp_paths = {("A", "B", "C")}

    obs_pathways = ap.find_simple_paths(G, sources, sinks)

    assert exp_paths == obs_pathways


def test_find_simple_paths_str_sinks():
    G = nx.MultiDiGraph()
    edges = [("Source","A"), ("A","B"), ("B","C"), ("B","Sink"), ("C","A")]
    G.add_edges_from(edges)
    sources = ["Source"]
    sinks = "Sink"
    exp_paths = {("Source","A","B","Sink")}

    obs_pathways = ap.find_simple_paths(G, sources, sinks)

    assert exp_paths == obs_pathways


def test_find_simple_paths_int_sources():
    G = nx.MultiDiGraph()
    edges = [(0,1), (1,2), (2,3), (2,4), (3,1)]
    G.add_edges_from(edges)
    sources = 0
    sinks = [4]

    exp_paths = {(0, 1, 2, 4)}
    obs_pathways = ap.find_simple_paths(G, sources, sinks)

    assert exp_paths == obs_pathways


def test_find_simple_paths_int_sinks():
    G = nx.MultiDiGraph()
    edges = [(0,1), (1,2), (2,3), (2,4), (3,1)]
    G.add_edges_from(edges)
    sources = [0]
    sinks = 4

    exp_paths = {(0, 1, 2, 4)}
    obs_pathways = ap.find_simple_paths(G, sources, sinks)

    assert exp_paths == obs_pathways


@pytest.mark.parametrize("name, edges, fd_in, fd_out, exp_paths", testdata)
def test_apa(name, edges, fd_in, fd_out, exp_paths):
    (G, obs_paths) = ap.conduct_apa(fd_in, fd_out)

    assert obs_paths == exp_paths
