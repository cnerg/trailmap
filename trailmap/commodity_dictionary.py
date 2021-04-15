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
    - metadata: Cyclus metadata
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
            if param == "uitype":
                if uitype in agent_data[var][param]: #typical for archetypes
                    aliases.append(var)
                #if streams are present
                path = search_var_recursive(agent_data[var][param], uitype)
                if path is not None:
                    aliases.append(find_alias(agent_data[var]["alias"], path))

    #drop the "val" (signifing an interleave) and "streams_" aliases 
    try:
        while True:
            aliases.remove("val")
    except:
        pass
    try:
        while True:
            aliases.remove('streams_')
    except:
        pass

    return aliases


def search_var_recursive(var, uitype):
    '''Finds the path within streams_ or similar tree that matches desired
    uitype. Searches recursively

    inputs:
        - var: a nested list from an archetype's metadata
        - uitype: a string. Example, "incommodity"

    outputs:
        - path: the path within var that locates uitype
    '''
    for index,item in enumerate(var):
        if item == uitype:
            return [index]
        if isinstance(item, list):
            path = search_var_recursive(item, uitype)
            if path:
                return [index] + path


def find_alias(var, path):
    '''Given path to locate uitype, searches archetype aliases to locate
    matching alias

    inputs:
        - var: a nested list of aliases
        - path: the path to search for the desired alias

    outputs:
        - alias: a string
    '''
    if len(path) == 1:
        return var[path[0]]
    else:
        return find_alias(var[path[0]], path[1:])


def build_facility_dictionary(metadata, archetypes):
    '''Identify commodities for each available archetype
    
    inputs:
        - metadata: Cyclus metadata
        - archetypes: a list of archetypes to use

    outputs:
        - archetype_commods: a dictionary with the Cyclus archetypes available
        and the names of their incommodities and outcommodities 
    '''
    archetype_commods = {}

    for archetype in archetypes:
        incommods = get_commod_names(metadata["annotations"], "incommodity",
                                     archetype)
        outcommods = get_commod_names(metadata["annotations"], "outcommodity",
                                      archetype)



        archetype_commods.update({archetype: (incommods,
                                              outcommods)})

    return archetype_commods
