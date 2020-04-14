import os
import sys
from argparse import ArgumentParser

from apa import (APA, Graph, Vertex)


def run_apa(ns):
    """Conducts Acquisition Pathway Analysis when input file exists"""
    state = APA(input_arcs=ns.input_arcs, input_vertices=ns.input_vertices)
    [arc_list, vertex_list] = state.load_input()

    g = Graph()
    g.build_graph(arc_list, vertex_list)

    g.print_graph()


def make_parser():
    """Makes the Cyclus-APA parser"""
    p = ArgumentParser(description="Cyclus-APA command line",
                       epilog="python main.py -e arcs -v vertices")
    # p.add_argument('--input_file', dest='input_file', default=None,
    #                help='path to input file')
    p.add_argument('-e', dest='input_arcs', default=None)
    p.add_argument('-v', dest='input_vertices', default=None)
    # p.add_argument('--output_file', dest='output_file', default='apa.txt',
    #                help='path to output file')

    return p


def main(args=None):
    """Main function for Cyclus-APA CLI"""
    # parse args
    p = make_parser()
    ns = p.parse_args(args=args)
    if None not in (ns.input_arcs, ns.input_vertices):
        # if ns.input_arcs is not None & ns.input_vertices is not None:
        run_apa(ns)
    else:
        print('No inputs given!')


if __name__ == '__main__':
    main()
