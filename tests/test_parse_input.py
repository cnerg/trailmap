import pytest
import trailmap.parse_input as pi
import xml.etree.ElementTree as ET


def test_find_commod():
    tree = ET.parse('input/source_1_sink_1.xml')
    root = tree.getroot()
    exp_out_commods = ['commodity']
    obs_out_commods = []
    for archetype_var in root.find('./facility/config/Source'):
        obs_out_commods.extend(pi.find_commod(archetype_var, 'outcommod'))

    assert obs_out_commods == exp_out_commods


@pytest.mark.parametrize("exp_archetypes, test_file",
                         [({'Sink': ':cycamore:Sink',
                            'Source': ':cycamore:Source',
                            'NullRegion': ':agents:NullRegion',
                            'NullInst': ':agents:NullInst'},
                           'input/source_3_sink_2.xml'),
                          ({'Sink': ':cycamore:Sink',
                            'Source': ':cycamore:Source',
                            'Storage': ':cycamore:Storage',
                            'Reactor': ':cycamore:Reactor',
                            'Enrichment': ':cycamore:Enrichment',

                            'NullRegion': ':agents:NullRegion',
                            'NullInst': ':agents:NullInst'},
                           'input/toy_front_end.xml')])
def test_find_archetypes(exp_archetypes, test_file):
    tree = ET.parse(test_file)
    root = tree.getroot()

    obs_archetypes = pi.get_archetypes_in_input(root)

    assert obs_archetypes == exp_archetypes


def test_facility_dict_in():
    tree = ET.parse('input/source_1_sink_1.xml')
    root = tree.getroot()
    commod_dict = {':cycamore:Sink': (['in_commods'], []),
                   ':cycamore:Source': ([], ['outcommod'])}
    archetypes = {'Sink': ':cycamore:Sink', 'Source': ':cycamore:Source'}
    exp_in = {'SomeSource': [], 'SomeSink': ['commodity']}

    [obs_in, obs_out] = pi.get_facility_and_commod_names(root, archetypes,
                                                         commod_dict)

    assert obs_in == exp_in


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

    exp_out = {'Mine': ['nat_u'], 'Enrich': ['leu', 'tails'],
               'ClandestineEnrich': ['heu', 'tails'],
               'Reactor': ['used_fuel'], 'SpentFuelPool': [],
               'ClandestineSink': []}

    [obs_in, obs_out] = pi.get_facility_and_commod_names(root, archetypes,
                                                         commod_dict)

    assert obs_out == exp_out
