import io
import sys
import trailmap.pathway_analysis as pa
import networkx as nx
import pytest
from tests.pa_data import testdata
# name, short, long, semiconnect, hierarchy, edges, paths


def test_ndp():
    exp = {('mine', 'civ_enrich', 'heu_pu_collector'),
           ('mine', 'mil_enrich', 'heu_pu_collector')}

    G = nx.DiGraph()
    edges = [('mine', 'civ_enrich'), ('mine', 'mil_enrich'),
             ('civ_enrich', 'heu_pu_collector'), ('civ_enrich', 'reactor'),
             ('reactor', 'reprocess'), ('reprocess', 'heu_pu_collector'),
             ('mil_enrich', 'heu_pu_collector')]
    G.add_edges_from(edges)

    obs = pa.find_node_disjoint_paths(G, 'mine', 'heu_pu_collector')

    assert obs == exp


def test_maximum_flow_simple():
    exp = 3
    G = nx.DiGraph()
    G.add_edge('a', 'b', capacity=3)
    G.add_edge('b', 'c', capacity=4)
    G.add_edge('c', 'd', capacity=3)
    G.add_edge('b', 'd', capacity=10)
    (obs_path, obs) = pa.find_maximum_flow(G, 'a', 'd')

    assert obs == exp


def test_maximum_flow_multipaths():
    exp = 3
    G = nx.DiGraph()
    G.add_edge('a', 'd', capacity=1)
    G.add_edge('a', 'b', capacity=1)
    G.add_edge('a', 'c', capacity=1)
    G.add_edge('b', 'd', capacity=2)
    G.add_edge('c', 'd', capacity=5)
    (obs_path, obs) = pa.find_maximum_flow(G, 'a', 'd')

    assert obs == exp


@pytest.mark.parametrize("name, short, long, semiconnect, hierarchy, edges, \
                         paths", testdata)
def test_gp_semiconnected(name, short, long, semiconnect, hierarchy, edges,
                          paths, capsys):
    G = nx.MultiDiGraph()
    G.add_edges_from(edges)

    (num_path, obs_semiconnected, h) = pa.print_graph_parameters(G, paths)
    assert obs_semiconnected == semiconnect


@pytest.mark.parametrize("name, short, long, semiconnect, hierarchy, edges, \
                         paths", testdata)
def test_gp_hierarchy(name, short, long, semiconnect, hierarchy, edges, paths,
                      capsys):
    G = nx.MultiDiGraph()
    G.add_edges_from(edges)

    (num_path, semi, obs_hierarchy) = pa.print_graph_parameters(G, paths)
    assert pytest.approx(obs_hierarchy) == hierarchy


@pytest.fixture
def data():
    return testdata


def test_find_paths_with_source(data):
    exp_subset = {("SourceA", "Facility", "SinkA"),
                  ("SourceA", "Facility", "SinkB")}
    pathways = testdata[2][6]
    source = "SourceA"

    obs_subset = pa.find_paths_with_source(pathways, source)
    assert obs_subset == exp_subset


def test_find_paths_with_sink(data):
    exp_subset = {("SourceA", "Facility", "SinkB"),
                  ("SourceB", "Facility", "SinkB")}
    pathways = testdata[2][6]
    sink = "SinkB"

    obs_subset = pa.find_paths_with_sink(pathways, sink)
    assert obs_subset == exp_subset
