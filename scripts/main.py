from argparse import ArgumentParser
import parse_input as pi
import commodity_dictionary as cd


def make_parser():
    """Makes the Cyclus-APA command line parser"""
    p = ArgumentParser(description="Cyclus-APA command line",
                       epilog="python main.py -e arcs -v vertices")
    return p


def main(args=None):
    """Main function for Cyclus-APA CLI"""
    # parse args
    p = make_parser()
    ns = p.parse_args(args=args)

    input_file = 'source_3_sink_1.xml'

    if (input_file) is not None:
        commodity_dictionary = cd.build_commod_dictionary()
<<<<<<< HEAD
        facility_dictionary = pi.parse_input(input_file, commodity_dictionary)
=======
>>>>>>> move commodity dictionary to own file, parse independently of Cyclus input file
    else:
        print('No input file given!')


if __name__ == '__main__':
    main()
