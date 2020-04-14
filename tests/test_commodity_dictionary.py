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
