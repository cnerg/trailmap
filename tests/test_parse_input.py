import pytest
import trailmap.parse_input as pi
import xml.etree.ElementTree as ET


def test_find_commod():
    tree = ET.parse('input/source_1_sink_1.xml')
    root = tree.getroot()
    out_commod_tags = ['commodity']
    for archetype_var in root.find('./facility/config/Source'):
        commods = pi.find_commod(archetype_var, 'outcommod')

        assert out_commod_tags == commods
        break


def test_find_archetypes():
    tree = ET.parse('input/source_3_sink_2.xml')
    root = tree.getroot()
    archetypes = {'Sink': ':cycamore:Sink', 'Source': ':cycamore:Source',
                  'NullRegion': ':agents:NullRegion',
                  'NullInst': ':agents:NullInst'}
    assert archetypes == pi.get_archetypes_in_input(root)


def test_find_archetypes1():
    tree = ET.parse('input/toy_front_end.xml')
    root = tree.getroot()
    archetypes = {'Sink': ':cycamore:Sink', 'Source': ':cycamore:Source',
                  'Storage': ':cycamore:Storage',
                  'Reactor': ':cycamore:Reactor',
                  'Enrichment': ':cycamore:Enrichment',
                  'NullRegion': ':agents:NullRegion',
                  'NullInst': ':agents:NullInst'}

    assert archetypes == pi.get_archetypes_in_input(root)
