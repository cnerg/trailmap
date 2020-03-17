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
