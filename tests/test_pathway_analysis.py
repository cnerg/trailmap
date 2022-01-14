import io
import sys
import trailmap.pathway_analysis as pa
import networkx as nx
import pytest
from tests.pa_data import testdata
import collections
from math import inf
# name, short, long, semiconnect, hierarchy, edges, paths, sc


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


@pytest.mark.parametrize("source,target", [('import', 'heu_pu_collector'),
                                           ('mine', 'export'),
                                           ('import', 'export')])
def test_ndp_raise_exception(source, target):
    G = nx.DiGraph()
    edges = [('mine', 'civ_enrich'), ('mine', 'mil_enrich'),
             ('civ_enrich', 'heu_pu_collector'), ('civ_enrich', 'reactor'),
             ('reactor', 'reprocess'), ('reprocess', 'heu_pu_collector'),
             ('mil_enrich', 'heu_pu_collector')]
    G.add_edges_from(edges)

    with pytest.raises(ValueError) as excinfo:
        obj = pa.find_node_disjoint_paths(G, source, target)
        assert 'Source and/or target not in graph G!' in str(excinfo.value)


def test_is_multidigraph_true():
    exp = True
    G = nx.MultiDiGraph()
    G.add_edge('a', 'b')
    obs = pa.is_multidigraph(G)

    assert obs == exp


def test_is_multidigraph_graph():
    exp = False
    G = nx.Graph()
    G.add_edge('a', 'b')
    obs = pa.is_multidigraph(G)

    assert obs == exp


def test_is_multidigraph_digraph():
    exp = False
    G = nx.DiGraph()
    G.add_edge('a', 'b')
    obs = pa.is_multidigraph(G)

    assert obs == exp


def test_is_multidigraph_multigraph():
    exp = False
    G = nx.MultiGraph()
    G.add_edge('a', 'b')
    obs = pa.is_multidigraph(G)

    assert obs == exp


def test_has_multiedges_true():
    exp = True
    G = nx.MultiDiGraph()
    G.add_edge('a', 'b')
    G.add_edge('a', 'b')

    obs = pa.has_multiedges(G)
    assert obs == exp


def test_has_multiedges_false():
    exp = False
    G = nx.MultiDiGraph()
    G.add_edge('a', 'b')
    G.add_edge('a', 'c')

    obs = pa.has_multiedges(G)
    assert obs == exp


def test_has_multiedges_not_multigraph():
    exp = None
    G = nx.DiGraph()
    G.add_edge('a', 'b')

    obs = pa.has_multiedges(G)
    assert obs == exp


def test_transform_to_digraph():
    G = nx.MultiDiGraph()
    G.add_edge('a', 'b')
    exp_H = nx.DiGraph()
    exp_H.add_edge('a', 'b')
    exp = list(exp_H.edges())

    (obs_H, obs_safe) = pa.transform_to_digraph(G)
    obs = list(obs_H.edges())

    assert obs == exp


def test_transform_to_digraph_has_multiedges():
    G = nx.MultiDiGraph()
    G.add_edge('a', 'b')
    G.add_edge('a', 'b')
    exp = False

    (obs_H, obs_safe) = pa.transform_to_digraph(G)

    assert obs_safe == exp


@pytest.mark.parametrize("G", [(nx.Graph()), (nx.MultiGraph())])
def test_transform_to_digraph_unsafe(G):
    exp = False
    G.add_edge('a', 'b')
    G.add_edge('a', 'b')

    (obs_H, obs_safe) = pa.transform_to_digraph(G)

    assert obs_safe == exp


@pytest.mark.parametrize("G,exp", [(nx.Graph(), None),
                                   (nx.MultiGraph(), None)])
def test_transform_to_digraph_formats(G, exp):
    G.add_edge('a', 'b')
    (obs_H, obs_safe) = pa.transform_to_digraph(G)

    assert obs_H == exp


@pytest.mark.parametrize("G,exp", [(nx.Graph(), False),
                                   (nx.DiGraph(), True),
                                   (nx.MultiGraph(), False),
                                   (nx.MultiDiGraph(), True)])
def test_transform_to_digraph_formats_is_safe(G, exp):
    G.add_edge('a', 'b')
    (obs_H, obs_safe) = pa.transform_to_digraph(G)

    assert obs_safe == exp


def test_maximum_flow_simple():
    exp = 3
    G = nx.DiGraph()
    G.add_edge('a', 'b', capacity=3)
    G.add_edge('b', 'c', capacity=4)
    G.add_edge('c', 'd', capacity=3)
    G.add_edge('b', 'd', capacity=10)
    (obs_path, obs) = pa.find_maximum_flow(G, 'a', 'd')

    assert obs == exp


def test_maximum_flow_several_paths():
    exp = 3
    G = nx.DiGraph()
    G.add_edge('a', 'd', capacity=1)
    G.add_edge('a', 'b', capacity=1)
    G.add_edge('a', 'c', capacity=1)
    G.add_edge('b', 'd', capacity=2)
    G.add_edge('c', 'd', capacity=5)
    (obs_path, obs) = pa.find_maximum_flow(G, 'a', 'd')

    assert obs == exp


def test_maximum_flow_multigraph():
    '''NetworkX retains only the most recently added edge if multiple edges
    exit and a MultiGraph is converted into a DiGraph'''
    exp = 1
    G = nx.DiGraph()
    G.add_edge('a', 'b', capacity=2)
    G.add_edge('a', 'b', capacity=1)
    G.add_edge('b', 'c', capacity=5)

    (obs_path, obs) = pa.find_maximum_flow(G, 'a', 'c')

    assert obs == exp


def test_maximum_flow_multigraph_order_flipped():
    '''NetworkX retains only the most recently added edge if multiple edges
    exit and a MultiGraph is converted into a DiGraph'''
    exp = 2
    G = nx.DiGraph()
    G.add_edge('a', 'b', capacity=1)
    G.add_edge('a', 'b', capacity=2)
    G.add_edge('b', 'c', capacity=5)

    (obs_path, obs) = pa.find_maximum_flow(G, 'a', 'c')

    assert obs == exp


def test_maximum_flow_directed_only():
    exp = 5
    G = nx.DiGraph()
    G.add_edge('a', 'b', capacity=4)
    G.add_edge('a', 'c', capacity=4)
    G.add_edge('b', 'd', capacity=2)
    G.add_edge('b', 'e', capacity=1)
    G.add_edge('c', 'd', capacity=3)
    G.add_edge('d', 'e', capacity=4)

    (obs_path, obs) = pa.find_maximum_flow(G, 'a', 'e')

    assert obs == exp


def test_maximum_flow_not_directed_or_multi():
    exp = None
    G = nx.Graph()
    G.add_edge('a', 'b', capacity=2)
    G.add_edge('b', 'c', capacity=5)

    with pytest.raises(TypeError) as excinfo:
        (obs_path, obs) = pa.find_maximum_flow(G, 'a', 'c')
        assert 'Graph must be DiGraph type' in str(excinfo)


def test_find_pathway_flow():
    G = nx.DiGraph()
    edges = [(0, 1, {'capacity': 3}),
             (1, 2, {'capacity': 5}),
             (2, 3, {'capacity': 3}),
             (3, 4, {'capacity': 4}),
             (0, 5, {'capacity': 2}),
             (5, 6, {'capacity': 3}),
             (6, 3, {'capacity': 2}),
             (3, 7, {'capacity': 1}),
             (7, 4, {'capacity': 2})]
    G.add_edges_from(edges)
    path = (0, 5, 6, 3, 7)

    exp = 1
    obs = pa.find_pathway_flow(G, path)

    assert obs == exp


def test_find_pathway_flow_no_capacity():
    G = nx.DiGraph()
    edges = [(0, 1), (1, 2), (2, 3)]
    G.add_edges_from(edges)
    path = (0, 1, 2, 3)

    with pytest.raises(nx.exception.NetworkXUnbounded) as excinfo:
        obj = pa.find_pathway_flow(G, path)
        assert 'Infinite capacity path' in str(excinfo.value)


def test_find_pathway_flow_single_infinite():
    G = nx.DiGraph()
    edges = [(0, 1, {'capacity': 3}),
             (1, 2, {'capacity': inf}),
             (2, 3, {'capacity': 3})]
    G.add_edges_from(edges)
    path = (0, 1, 2, 3)
    obs = pa.find_pathway_flow(G, path)

    exp = 3

    assert obs == exp


def test_find_pathway_flow_all_infinite():
    G = nx.DiGraph()
    edges = [(0, 1, {'capacity': inf}),
             (1, 2, {'capacity': inf}),
             (2, 3, {'capacity': inf})]
    G.add_edges_from(edges)
    path = (0, 1, 2, 3)

    with pytest.raises(nx.exception.NetworkXUnbounded) as excinfo:
        obj = pa.find_pathway_flow(G, path)
        assert 'Infinite capacity path' in str(excinfo.value)


def test_find_pathway_flow_multiedges():
    G = nx.MultiDiGraph()
    edges = [(0, 1), (1, 2), (1, 2), (2, 3)]
    G.add_edges_from(edges)
    pathway = (0, 1, 2, 3)

    with pytest.raises(TypeError) as excinfo:
        obs = pa.find_pathway_flow(G, pathway)
        assert 'Graph must be DiGraph type. Use' in str(excinfo)


def test_find_pathway_flow_other_type():
    G = nx.Graph()
    edges = [(0, 1), (1, 2), (2, 3)]
    G.add_edges_from(edges)
    pathway = (0, 1, 2, 3)

    with pytest.raises(TypeError) as excinfo:
        obs = pa.find_pathway_flow(G, pathway)
        assert 'Graph must be DiGraph type' in str(excinfo)


@pytest.mark.parametrize("steps,exp", [(('FacilityA', 'FacilityB'), 1),
                                       (('FacilityA', 'Sink'), -1)])
def test_check_if_sublist(steps, exp):
    path = ('Source', 'FacilityA', 'FacilityB', 'Sink')
    pos = pa.check_if_sublist(path, steps)
    assert pos == exp


@pytest.mark.parametrize("path,steps,exp", [(('Source', 'Sink'), (), -1),
                                            ((), ('Sink'), -1)])
def test_check_if_sublist_len_zero(path, steps, exp):
    path = ('Source', 'FacilityA', 'FacilityB', 'Sink')
    pos = pa.check_if_sublist(path, steps)
    assert pos == exp


@pytest.mark.parametrize("cycle,exp", [([3, 4, 7], (7, 3, 4)),
                                       ([7, 3, 4], (7, 3, 4)),
                                       ([5, 6], None),
                                       ([6], None),
                                       ([], None)])
def test_roll_cycle(cycle, exp):
    path = (0, 1, 3, 4, 7, 8)

    obs = pa.roll_cycle(path, cycle)
    assert obs == exp


def test_insert_cycle_single():
    path = (0, 1, 3, 4, 7, 8)
    rolled_cycles = {(7, 3, 4)}

    exp = (0, 1, 3, 4, (7, 3, 4), 7, 8)
    obs = pa.insert_cycles(path, rolled_cycles)
    assert obs == exp


def test_insert_cycle_loop():
    path = (0, 1, 3, 4, 7, 8)
    rolled_cycles = {(7,)}

    exp = (0, 1, 3, 4, (7,), 7, 8)
    obs = pa.insert_cycles(path, rolled_cycles)
    assert obs == exp


def test_insert_cycle_multiple():
    path = (0, 2, 6, 7, 8)
    rolled_cycles = ((6, 5), (7, 3, 4))

    exp = (0, 2, (6, 5), 6, (7, 3, 4), 7, 8)
    obs = pa.insert_cycles(path, rolled_cycles)
    assert obs == exp


def test_insert_cycle_multiple_same_index():
    path = ('Source', 'A', 'B', 'C', 'Sink')
    rolled_cycles = (('C', 'D', 'B'), ('C', 'D', 'E', 'A', 'B'))

    exp = ('Source', 'A', 'B', ('C', 'D', 'B'), ('C', 'D', 'E', 'A', 'B'),
           'C', 'Sink')
    obs = pa.insert_cycles(path, rolled_cycles)
    assert obs == exp


def test_insert_cycle_multiple_same_index_with_loop():
    path = (0, 2, 6, 7, 8)
    rolled_cycles = {(7,), (7, 3, 4)}

    exp = (0, 2, 6, (7,), (7, 3, 4), 7, 8)
    obs = pa.insert_cycles(path, rolled_cycles)
    assert obs == exp


def test_get_pathways_with_cycles():
    pathways = {(0, 1, 3, 4, 7, 8)}
    sc = [[2, 1]]

    exp = {(0, (1, 2), 1, 3, 4, 7, 8)}
    obs = pa.get_pathways_with_cycles(pathways, sc)

    assert obs == exp


def test_get_pathways_with_cycles_multiple():
    pathways = {(0, 1, 3, 4, 7, 8), (0, 2, 3, 4, 7, 8), (0, 2, 6, 7, 8)}
    sc = [[5, 6], [3, 4, 7]]

    exp = {(0, 1, 3, 4, (7, 3, 4), 7, 8),
           (0, 2, 3, 4, (7, 3, 4), 7, 8),
           (0, 2, (6, 5), 6, (7, 3, 4), 7, 8)}

    obs = pa.get_pathways_with_cycles(pathways, sc)
    # assert all(x in obs for x in exp)
    assert obs == exp


def test_get_pathways_with_cycles_loop():
    pathways = {(0, 1, 3, 4, 7, 8), (0, 2, 3, 4, 7, 8), (0, 2, 6, 7, 8)}
    sc = [[7], [3, 4, 7]]

    exp = {(0, 1, 3, 4, (7, 3, 4), (7,), 7, 8),
           (0, 2, 3, 4, (7, 3, 4), (7,), 7, 8),
           (0, 2, 6, (7, 3, 4), (7,), 7, 8)}

    obs = pa.get_pathways_with_cycles(pathways, sc)
    assert obs == exp


def test_get_pathways_with_cycles_none():
    pathways = []
    obs = pa.get_pathways_with_cycles(pathways, [[2, 1]])

    assert obs == set()


def data():
    return testdata


@pytest.mark.parametrize("source,exp", [("SourceA",
                                        {("SourceA", "Facility", "SinkA"),
                                         ("SourceA", "Facility", "SinkB")}),
                                        ("SourceC", set()),
                                        ("Facility", set())])
def test_find_paths_with_source(source, exp):
    pathways = testdata[2][4]

    obs_subset = pa.find_paths_with_source(pathways, source)
    assert obs_subset == exp


def test_find_paths_with_source_none():
    pathways = []
    obs = pa.find_paths_with_source(pathways, "SourceA")

    assert obs == set()


@pytest.mark.parametrize("sink,exp", [("SinkB",
                                      {("SourceA", "Facility", "SinkB"),
                                       ("SourceB", "Facility", "SinkB")}),
                                      ("SinkC", set()),
                                      ("SourceA", set())])
def test_find_paths_with_sink(sink, exp):
    pathways = testdata[2][4]

    obs_subset = pa.find_paths_with_sink(pathways, sink)
    assert obs_subset == exp


def test_find_paths_with_sink_none():
    pathways = []
    obs = pa.find_paths_with_sink(pathways, "SinkA")

    assert obs == set()


@pytest.mark.parametrize("contain,exp", [("SourceB",
                                         {("SourceB", "Facility", "SinkA"),
                                          ("SourceB", "Facility", "SinkB")}),
                                         (["SourceB", "SinkB"],
                                         {("SourceB", "Facility", "SinkB")}),
                                         (["SourceB", "SourceA"], set()),
                                         ([], set())])
def test_find_paths_containing_all(contain, exp):
    pathways = testdata[2][4]

    obs = pa.find_paths_containing_all(pathways, contain)
    assert obs == exp


@pytest.mark.parametrize("contain,exp", [(5, {(0, 1, 5, 6, 4)}),
                                         ([5], {(0, 1, 5, 6, 4)}),
                                         ([1, 5], {(0, 1, 5, 6, 4)}),
                                         ([0, 3], {(0, 1, 2, 3, 4),
                                                   (0, 2, 3, 4)}),
                                         ([5, 7], set()),
                                         ([8], set()),
                                         ([7, 8], set()),
                                         ([], set())])
def test_find_paths_containing_all_int(contain, exp):
    pathways = {(0, 1, 2, 3, 4), (0, 2, 3, 4), (0, 1, 5, 6, 4), (0, 1, 7, 4)}

    obs = pa.find_paths_containing_all(pathways, contain)
    assert obs == exp


def test_find_paths_containing_all_none():
    pathways = []
    obs = pa.find_paths_containing_all(pathways, "SinkA")

    assert obs == set()


@pytest.mark.parametrize("contain,exp", [("SourceA",
                                         {("SourceA", "Facility", "SinkA"),
                                          ("SourceA", "Facility", "SinkB")}),
                                         (["SourceA", "SinkA"],
                                         {("SourceA", "Facility", "SinkA"),
                                          ("SourceA", "Facility", "SinkB"),
                                          ("SourceB", "Facility", "SinkA")}),
                                         (["SourceC"], set()),
                                         ([], set())])
def test_find_paths_containing_one_of(contain, exp):
    pathways = testdata[2][4]

    obs = pa.find_paths_containing_one_of(pathways, contain)
    assert obs == exp


@pytest.mark.parametrize("contain,exp", [(5, {(0, 1, 5, 6, 4)}),
                                         ([5], {(0, 1, 5, 6, 4)}),
                                         ([5, 7], {(0, 1, 5, 6, 4),
                                                   (0, 1, 7, 4)}),
                                         (8, set()),
                                         ([8], set()),
                                         ([7, 8], {(0, 1, 7, 4)}),
                                         ([], set())])
def test_find_paths_containing_one_of_int(contain, exp):
    pathways = {(0, 1, 2, 3, 4), (0, 2, 3, 4), (0, 1, 5, 6, 4), (0, 1, 7, 4)}

    obs = pa.find_paths_containing_one_of(pathways, contain)
    assert obs == exp


def test_get_shortest_path_length_none():
    pathways = {}
    exp = set()
    obs = pa.get_shortest_path(pathways)

    assert obs == exp


@pytest.mark.parametrize("name, short, long, edges, paths, sc", testdata)
def test_get_shortest_paths(name, short, long, edges, paths, sc):
    exp = {path for path in paths if len(path) == short}
    obs = pa.get_shortest_path(paths)
    assert obs == exp


def test_get_longest_path_length_none():
    pathways = {}
    exp = set()
    obs = pa.get_longest_path(pathways)

    assert obs == exp


@pytest.mark.parametrize("name, short, long, edges, paths, sc", testdata)
def test_get_longest_paths(name, short, long, edges, paths, sc):
    exp = {path for path in paths if len(path) == long}
    obs = pa.get_longest_path(paths)
    assert obs == exp


def test_sort_shortest():
    pathways = {(2 3), (3, 4, 7, 4, 3, 32, 3), (10000, 10000, 0)}
    exp = [(2, 3), (10000, 10000, 0), (3, 4, 7, 4, 3, 32, 3)]

    obs = pa.sort_by_shortest(pathways)
    assert obs == exp


def test_sort_longest():
    pathways = {(2 3), (3, 4, 7, 4, 3, 32, 3), (10000, 10000, 0)}
    exp = [(3, 4, 7, 4, 3, 32, 3), (10000, 10000, 0), (2, 3)]

    obs = pa.sort_by_longest(pathways)
    assert obs == exp


@pytest.mark.parametrize("pathways", [{("a", "b")},
                                      {("a", "b"), (1, "b")},
                                      {(1, 4)},
                                      {(4, 5), (6, 5.9)},
                                      {(6.3, "a")}])
def test_check_for_invalid_pathways(pathways):
    obs = pa.check_for_invalid_pathways(pathways)
    assert obs is None


@pytest.mark.parametrize("pathways", [{("a")},
                                      {("a", "b"), "c"},
                                      {(1)},
                                      {(4, 5), 6},
                                      {(6.3, "a"), 4.6},
                                      {(5.3)}])
def test_check_for_invalid_pathways_type_error(pathways):
    with pytest.raises(TypeError) as excinfo:
        obj = pa.sort_by_longest(pathways)
        assert 'pathways contains' in str(excinfo.value)
