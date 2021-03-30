import argparse
import networkx as nx
import trailmap.parse_input as pi
import trailmap.commodity_dictionary as cd
import trailmap.acquisition_paths as ap
import trailmap.pathway_analysis as pa


def make_parser():
    """Makes the Cyclus-Trailmap command line parser"""
    p = argparse.ArgumentParser(description="Cyclus-Trailmap command line",
                                epilog="python main.py cyclus_input_file.xml")
    p.add_argument('infile', nargs=1, help='Cyclus input file. Must be XML')
    p.add_argument('--draw', '-d', action='store_true')
    p.add_argument('--pickle', '-pi', action='store_true',
                   help="pickle graph output of fuel cycle")
    p.add_argument('--pickle-file', dest='picklefile',
                   default='trailmap.gpickle',
                   help='output path for pickled graph')
    p.add_argument('--supress-print', '-sp', action='store_true')
    p.add_argument('--metadata', '-m', nargs=1, help='Cyclus metadata file',
                   type=argparse.FileType('r'))

    return p


def main(args=None):
    """Main function for Cyclus-Trailmap CLI"""
    p = make_parser()
    ns = p.parse_args(args=args)

    if ns.metadata:
        m = ns.metadata[0]
        commodity_dictionary = cd.build_commod_dictionary(ns.metadata[0])
    else:
        commodity_dictionary = cd.build_commod_dictionary()
    (facility_dict_in,
    facility_dict_out) = pi.parse_input(ns.infile[0], commodity_dictionary)
    (G, pathways) = ap.conduct_apa(facility_dict_in, facility_dict_out)

    if ns.supress_print is False:
        pa.print_graph_parameters(G, pathways)
        ap.print_acquisition_paths(pathways)

    if ns.pickle:
        nx.write_gpickle(G, ns.picklefile)

    return G, pathways


if __name__ == '__main__':
    main()
