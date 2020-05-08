import os
import sys
import subprocess
import json
import xml.etree.ElementTree as ET
import cyclus


def parse_input(input, commodity_dictionary):
    '''Builds dicionary of facilities and their incommodies and outcommodities.

    inputs:
        - input: a Cyclus XML input file
        - commodity_dictionary: a dictionary

    outputs:
        - facility_dictionary: a dictionary of each facility and its
        incommodities and outcommodities. format:
        {'facility' : (['incommodities'], ['outcommodities'])}
    '''

    tree = ET.parse(input)
    root = tree.getroot()

    archetypes_in_input = get_archetypes_in_input(root)
    facility_dictionary = get_facility_and_commod_names(root,
                                                        archetypes_in_input,
                                                        commodity_dictionary)

    return facility_dictionary


def get_facility_and_commod_names(root, archetypes_in_input,
                                  commodity_dictionary):
    '''reads Cyclus input file element tree and finds the facility names for
    each facility specified in a <facility> tag. Uses the facility archetype
    and module, the input and output commodities are retrieved.

    inputs:
        - root: root of a Cyclus input file tree
        - archetypes_in_input: a dictionary
        - commodity_dictionary: a dictionary
    outputs:
        - facility_dict: a dictionary of each facility and its
        incommodities and outcommodities. format:
        {'facility' : (['incommodities'], ['outcommodities'])}
    '''
    facility_dict = {}

    for facility in root.findall('./facility'):
        facility_name = facility.find('name').text
        facility_archetype = facility.find('config/').tag
        facility_module = get_archetypes_in_input[facility_archetype]
        commodities = commodity_dictionary[facility_module]

        in_commod_tags = commodities[0]
        out_commod_tags = commodities[1]

#     (in_commod_tags, out_commod_tags) = commodity_dictionary[facility_module]

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


def get_archetypes_in_input(root):
    '''Finds the modules and archetypes that are defined in the archetypes tag.

    inputs:
        - root: root of a Cyclus input file tree

    outputs:
        - archetypes_in_input: a dictionary with format
                               {'archetype' : 'module::archetype'}
    '''
    archetypes_in_input = {}
    for archetype in root.findall('./archetypes/'):
        for library in archetype.findall('./lib'):
            lib = library.text
        for archetypename in archetype.findall('./name'):
            name = archetypename.text

        library_and_archetype = (':%s:%s' % (lib, name))
        archetypes_in_input[name] = library_and_archetype

    return archetypes_in_input


def find_commod(archetype_tag, commod_tags):
    '''Searches for commodities within an acceptable list of commodity tags.
    Returns None if none found

    inputs:
        - archetype_tag: a single archetype tag
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
