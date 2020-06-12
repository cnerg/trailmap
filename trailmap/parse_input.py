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

    input_archetypes = get_archetypes_in_input(root)
    [facility_dict_in,
     facility_dict_out] = get_facility_and_commod_names(root, input_archetypes,
                                                        commodity_dictionary)

    return facility_dict_in, facility_dict_out


def get_facility_and_commod_names(root, input_archetypes,
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
    facility_dict_in = {}
    facility_dict_out = {}

    for facility in root.findall('./facility'):
        facility_name = facility.find('name').text
        facility_archetype = facility.find('config/').tag
        facility_module = input_archetypes[facility_archetype]

        if facility_module == ':cycamore:Separations':
            (facility_in_commods,
             facility_out_commods) = find_sep_commod(facility,
                                                     facility_archetype)
        else:
            (in_tags, out_tags) = commodity_dictionary[facility_module]
            facility_in_commods = []
            facility_out_commods = []

            for archetype_var in facility.find('.config/'+facility_archetype):
                in_commods = find_commod(archetype_var, in_tags)
                if in_commods is not None:
                    facility_in_commods.extend(in_commods)

                out_commods = find_commod(archetype_var, out_tags)
                if out_commods is not None:
                    facility_out_commods.extend(out_commods)

        facility_dict_in[facility_name] = facility_in_commods
        facility_dict_out[facility_name] = facility_out_commods

    return facility_dict_in, facility_dict_out


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

    return commod_list


def find_sep_commod(facility, facility_archetype):
    '''Searches for commodities within a Separations facility, which uses a
    different xml schema than other Cyclus archetypes
    '''
    in_tags = ['feed_commods']
    leftover_tags = ['leftover_commod']
    out_tags = ["commod"]

    facility_in_commods = []
    facility_out_commods = []

    for archetype_var in facility.find('.config/' + facility_archetype):
        in_commods = find_commod(archetype_var, in_tags)
        if in_commods is not None:
            facility_in_commods.extend(in_commods)
        if archetype_var.tag == 'streams':
            for commod in archetype_var.findall('./item/commod'):
                facility_out_commods.append(commod.text)

    return facility_in_commods, facility_out_commods
