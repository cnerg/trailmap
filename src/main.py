from argparse import ArgumentParser
import parse_input as pi


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
        pi.parse_input(input_file)
    else:
        print('No input file given!')


if __name__ == '__main__':
    main()
