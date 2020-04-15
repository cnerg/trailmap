import argparse
import parse_input as pi
import commodity_dictionary as cd


def make_parser():
    """Makes the Cyclus-Trailmap command line parser"""
    p = argparse.ArgumentParser(description="Cyclus-Trailmap command line",
                                epilog="python main.py cyclus_input_file.xml")
    p.add_argument('infile', nargs=1, help='Cyclus input file. Must be XML')

    return p


def main(args=None):
    """Main function for Cyclus-Trailmap CLI"""
    p = make_parser()
    ns = p.parse_args(args=args)

    if ns.infile[0] is not None:
        commodity_dictionary = cd.build_commod_dictionary()
        facility_dictionary = pi.parse_input(ns.infile[0],
                                             commodity_dictionary)
    else:
        print('No input file given!')


if __name__ == '__main__':
    main()
