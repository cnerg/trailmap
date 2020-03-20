import os
import sys
import subprocess
import json
import xml.etree.ElementTree as ET
import cyclus


def parse_input(input, commodity_dictionary):
    '''
    archetype_commods = parse_input(input, commodity_dictionary)

    inputs:
        - input: a Cyclus XML input file
        - commodity_dictionary: a dictionary with the Cyclus archetypes
        available and the archetype tags of their incommodities and
        outcommodities

    outputs:
        - facility_dictionary: a dictionary of each facility and its
        incommodities and outcommodities. format:
        {'facility' : (['incommodities'], ['outcommodities'])}
    '''

    tree = ET.parse(input)
    root = tree.getroot()

    archetypes_in_input = archetypes_in_input_file(root)
    facility_dictionary = get_facility_and_commod_names(root,
                                                        archetypes_in_input,
                                                        commodity_dictionary)

    return facility_dictionary


def get_facility_and_commod_names(root, archetypes_in_input,
                                  commodity_dictionary):
    '''
    facility_dict = get_facility_and_commod_names(root, archetypes_in_input,
                                    commodity_dictionary)

    get_facility_and_commodity_names reads a Cyclus input file element tree and
    finds the facility names for each facility specified in a <facility> tag.
    Then, using the facility archetype and module, the input and output
    commodities are retrieved.

    inputs:
        - root: an xml.etree.ElementTree root of a Cyclus input file tree
        - archetypes_in_input: a dictionary with format
                               {'archetype' : 'module::archetype'}
        - commodity_dictionary: a dictionary with the Cyclus archetypes
        available and the archetype tags of their incommodities and
        outcommodities

    outputs:
        - facility_dict: a dictionary of each facility and its
        incommodities and outcommodities. format:
        {'facility' : (['incommodities'], ['outcommodities'])}
    '''

    facility_dict = {}

    for facility in root.findall('./facility'):
        facility_name = facility.find('name').text
        facility_archetype = facility.find('config/').tag
        facility_module = archetypes_in_input[facility_archetype]
        commodities = commodity_dictionary[facility_module]

        in_commod_tags = commodities[0]
        out_commod_tags = commodities[1]

        facility_in_commods = []
        facility_out_commods = []

        for archetype_tag in facility.find('.config/' + facility_archetype):

            in_commods = find_commod(archetype_tag, in_commod_tags)
            if in_commods is not None:
                facility_in_commods.extend(in_commods)

            out_commods = find_commod(archetype_tag, out_commod_tags)
            if out_commods is not None:
                facility_out_commods.extend(out_commods)

        facility_dict[facility_name] = (facility_in_commods,
                                        facility_out_commods)

    return facility_dict


def archetypes_in_input_file(root):
    '''
    input_archetypes = archetypes_in_input_file(root)

    archetypes_in_input_file reads a Cyclus input file element tree and finds
    the modules and archetypes that are defined in the <archetypes> tag.

    inputs:
        - root: an xml.etree.ElementTree root of a Cyclus input file tree

    outputs:
        - archetypes_in_input: a dictionary with format
                               {'archetype' : 'module::archetype'}
    '''

    archetypes_in_input = {}
    for archetypes in root.findall('./archetypes/'):
        for library in archetypes.findall('./lib'):
            lib = library.text
        for name in archetypes.findall('./name'):
            name = name.text

        library_and_archetype = (':%s:%s' % (lib, name))
        archetypes_in_input[name] = library_and_archetype

    return archetypes_in_input


def find_commod(archetype_tag, commod_tags):
    '''
    commods = find_commod(archetype_tag, commod_tags)

    find_commod takes a single archetype tag within a Cyclus facility and
    searches for commodities within an acceptable list of commodity tags. Finds
    commodities whether they are text between the commodity tags e.g.
    <commod_tag>commodity</commod_tag> or within a child val tag
    e.g. <commod_tag>
            <val>commodity</val>
        </commod_tag>
    Returns None if none found

    inputs:
        - archetype_tag: an xml.etree.ElementTree.Element of a single archetype
        tag
        - commod_tags: a list of acceptable commodity tags for the given
        module and facility

    outputs:
        - commods: a single commodity as a string or a list of commodities
    '''

    commod_list = []

    if archetype_tag.tag in commod_tags:
        vals = archetype_tag.findall('./')
        if vals:
            for commod in vals:
                commod_list.append(commod.text)
        else:
            commod_list.append(archetype_tag.text)
        return commod_list

    return
