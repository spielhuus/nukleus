import argparse
from json import load
import sys

from nukleus import bom, load_schema, plot

def main() -> int:
    """Echo the input arguments to standard output"""
    parser = argparse.ArgumentParser(
        description='Nukleus electronic processing.')
    parser.add_argument('--bom', dest='action', action='append_const', const='bom',
                        help='Output the BOM as JSON')
    parser.add_argument('--plot', dest='action', action='append_const', const='plot',
                        help='Plot the Schema')
    parser.add_argument('--input', dest='input',
                        help='The input filename.')
    parser.add_argument('--output', dest='output',
                        help='The output filename.')

    args = parser.parse_args()
    print(args)

    schema = load_schema(args.input)

    for action in args.action:
        if action == 'bom':
            bom_res = bom(schema)
            print(bom_res)
        if action == 'plot':
            if args.output is None:
                print('Output file is required for plot schematic.')
                sys,exit(1)
            plot(schema, args.output, border=True)

    return 0

if __name__ == '__main__':
    sys.exit(main())
