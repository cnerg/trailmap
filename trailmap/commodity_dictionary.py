import os
import sys
import json
import cyclus


def build_commod_dictionary(metadata_file = None): #pragma: no cover
    '''Find all Cyclus archetypes and their commodity tags.

    outputs:
    - archetype_commods: a dictionary with the Cyclus archetypes available
        and the names of their incommodities and outcommodities
    '''
    if metadata_file is None:
        print('generating metadata')
        metadata = cyclus.lib.discover_metadata_in_cyclus_path()
    else: 
        metadata = json.load(metadata_file)

    archetypes = metadata["specs"]    
    archetype_commods = build_facility_dictionary(metadata, archetypes)

    return archetype_commods


def get_commod_names(metadata, uitype, agent):
    '''Return all archetypes and their aliases for a given uitype.

    inputs:
    - metadata
    - uitype: a string. Example, "incommodity"
    - agent: a string. Example, ":cycamore:Enrichment"

    outputs:
    - commods: dict with archetypes as keys and a set of acceptable aliases as
    the values
    '''
    agent_data = metadata[agent]["vars"]
    aliases = []

    for var in agent_data:
        for param in agent_data[var]:
            if param == "uitype" and uitype in agent_data[var][param]:
                aliases.append(var)

    return aliases


def build_facility_dictionary(metadata, archetypes):
    '''Identify commodities for each available archetype'''
    archetype_commods = {}

    for archetype in archetypes:
        incommods = get_commod_names(metadata["annotations"], "incommodity",
                                     archetype)
        outcommods = get_commod_names(metadata["annotations"], "outcommodity",
                                      archetype)

        archetype_commods.update({archetype: (incommods,
                                              outcommods)})

    return archetype_commods
