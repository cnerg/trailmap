import pytest
import trailmap.parse_input as pi
import xml.etree.ElementTree as ET


def test_find_commod():
    tree = ET.parse('input/source_1_sink_1.xml')
    root = tree.getroot()
    out_commod_tags = ['commodity']
    commods = []
    for archetype_var in root.find('./facility/config/Source'):
        commods.extend(pi.find_commod(archetype_var, 'outcommod'))

    assert out_commod_tags == commods


def test_find_archetypes():
    tree = ET.parse('input/source_3_sink_2.xml')
    root = tree.getroot()
    archetypes = {'Sink': ':cycamore:Sink', 'Source': ':cycamore:Source',
                  'NullRegion': ':agents:NullRegion',
                  'NullInst': ':agents:NullInst'}
    assert archetypes == pi.get_archetypes_in_input(root)


def test_find_archetypes1():
    tree = ET.parse('input/toy_front_end.xml')
    root = tree.getroot()
    archetypes = {'Sink': ':cycamore:Sink', 'Source': ':cycamore:Source',
                  'Storage': ':cycamore:Storage',
                  'Reactor': ':cycamore:Reactor',
                  'Enrichment': ':cycamore:Enrichment',
                  'NullRegion': ':agents:NullRegion',
                  'NullInst': ':agents:NullInst'}

    assert archetypes == pi.get_archetypes_in_input(root)


def test_facility_dict_in():
    tree = ET.parse('input/source_1_sink_1.xml')
    root = tree.getroot()
    commod_dict = {':cycamore:Sink': (['in_commods'], []),
                   ':cycamore:Source': ([], ['outcommod'])}
    archetypes = {'Sink': ':cycamore:Sink', 'Source': ':cycamore:Source'}
    [dict_in, dict_out] = pi.get_facility_and_commod_names(root,
                                                           archetypes,
                                                           commod_dict)
    test_in = {'SomeSource': [], 'SomeSink': ['commodity']}

    assert dict_in == test_in


def test_facility_dict_out():
    tree = ET.parse('input/toy_front_end.xml')
    root = tree.getroot()
    commod_dict = {':cycamore:Enrichment': (['feed_commod'], ['product_commod',
                                                              'tails_commod']),
                   ':cycamore:Reactor': (['fuel_incommods',
                                          'pref_change_commods',
                                          'recipe_change_commods'],
                                         ['fuel_outcommods']),
                   ':cycamore:Sink': (['in_commods'], []),
                   ':cycamore:Source': ([], ['outcommod']),
                   ':cycamore:Storage': (['in_commods'], ['out_commods'])}

    archetypes = {'Sink': ':cycamore:Sink', 'Source': ':cycamore:Source',
                  'Storage': ':cycamore:Storage',
                  'Reactor': ':cycamore:Reactor',
                  'Enrichment': ':cycamore:Enrichment'}

    [dict_in, dict_out] = pi.get_facility_and_commod_names(root,
                                                           archetypes,
                                                           commod_dict)
    test_out = {'Mine': ['nat_u'], 'Enrich': ['leu', 'tails'],
                'ClandestineEnrich': ['heu', 'tails'],
                'Reactor': ['used_fuel'], 'SpentFuelPool': [],
                'ClandestineSink': []}

    assert dict_out == test_out
