import trailmap.commodity_dictionary as cd
import pytest
import json


with open('tests/metadata.json') as f:
    metadata = json.load(f)
specs = metadata["specs"]


def test_commod_names_incommodity():
    '''Test the function get_commod_names for commodities entering a facility.
    '''
    assert ['in_commods'] == cd.get_commod_names(metadata["annotations"],
                                                 "incommodity",
                                                 ':cycamore:Storage')


def test_commod_names_outcomodity():
    '''Test the function get_commod_names for commodities exiting a facility.
    '''
    assert ['fuel_outcommods'] == cd.get_commod_names(metadata["annotations"],
                                                      "outcommodity",
                                                      ":cycamore:Reactor")


def test_build_facility_dictionary():
    exp = {':agents:KFacility': (['in_commod'], ['out_commod']),
           ':agents:NullInst': ([], []),
           ':agents:NullRegion': ([], []),
           ':agents:Predator': (['prey'], ['commod']),
           ':agents:Prey': ([], ['commod']),
           ':agents:Sink': (['in_commods'], []),
           ':agents:Source': ([], ['commod']),
           ':cycamore:DeployInst': ([], []),
           ':cycamore:Enrichment': (['feed_commod'], ['product_commod',
                                     'tails_commod']),
           ':cycamore:FuelFab': (['fill_commods', 'fiss_commods',
                                  'topup_commod'], ['outcommod']),
           ':cycamore:GrowthRegion': ([], []),
           ':cycamore:ManagerInst': ([], []),
           ':cycamore:Mixer': ([], ['out_commod']),
           ':cycamore:Reactor': (['fuel_incommods', 'pref_change_commods',
                                  'recipe_change_commods'],
                                 ['fuel_outcommods']),
           ':cycamore:Separations': (['feed_commods'], ['leftover_commod',
                                      'streams_']),
           ':cycamore:Sink': (['in_commods'], []),
           ':cycamore:Source': ([], ['outcommod']),
           ':cycamore:Storage': (['in_commods'], ['out_commods'])}

    assert cd.build_facility_dictionary(metadata, specs) == exp


def test_build_facility_dictionary_subset():
    archetypes = [':cycamore:Sink', ':cycamore:Source', ':cycamore:Storage']
    exp = {':cycamore:Sink': (['in_commods'], []), 
           ':cycamore:Source': ([], ['outcommod']),
            ':cycamore:Storage': (['in_commods'], ['out_commods'])}

    assert cd.build_facility_dictionary(metadata, archetypes) == exp
    
