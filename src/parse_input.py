import os
import sys
import subprocess
import json
import xml.etree.ElementTree as ET
import cyclus
from cyclus import lib
import pprint


def parse_input(input):
    '''
    '''

    tree = ET.parse(input)
    root = tree.getroot()

    # nodes = get_nodes_list(root)

    metadata_full = dump_metadata()
    archetype_commods = build_facility_dictionary(metadata_full)

    return archetype_commods


def get_nodes_list(root):
    '''
    '''

    nodes = []
    for facility in root.findall('./facility/name'):
        # print(facility.text)
        nodes.append(facility.text)

    return nodes


def dump_metadata():
    '''
    metadata = dump_metadata()
    Dumps Cyclus metadata via Cylus python interface and saves the output.
    Requires a working Cyclus install.

    output:
        - metadata
    '''

    metadata = lib.discover_metadata_in_cyclus_path()

    return metadata


def get_commod_names(metadata, uitype, agent):
    '''
    aliases = get_commod_alias(metadata, uitype, agent)
    Returns all archetypes and their aliases for a given uitype

    inputs:
        - metadata
        - uitype: a string. Example, "incommodity"
        - agent: a string. Example, ":cycamore:Enrichment"

    outputs:
        - commods: a dictionary with archetypes as keys and a set of acceptable
        aliases as the values
    '''

    agent_data = metadata[agent]["vars"]
    aliases = []

    for var in agent_data:
        for param in agent_data[var]:
            if param == "uitype" and uitype in agent_data[var][param]:
                aliases.append(var)

    return aliases


def commodity_aliases(data, aliases):
    '''
    Usage: run in get_commod_alias
    aliases = commodity_aliases(data, aliases)
    '''

    if isinstance(data, cyclus.jsoncpp.Value):
        aliases.extend(data)
    elif isinstance(data, str):
        aliases.append(data)

    return aliases


def build_facility_dictionary(metadata_full):
    '''
    Traverses all
    '''

    metadata = metadata_full["annotations"]
    specs = metadata_full["specs"]

    archetype_commods = {}

    for archetype in specs:
        incommod_aliases = get_commod_names(metadata, "incommodity", archetype)
        outcommod_aliases = get_commod_names(metadata, "outcommodity",
                                             archetype)

        archetype_commods.update({archetype: (incommod_aliases,
                                              outcommod_aliases)})

    pprint.pprint(archetype_commods)

    return archetype_commods
