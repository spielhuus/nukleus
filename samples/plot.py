import sys
import argparse


sys.path.append('src')
sys.path.append('../src')

import nukleus as nl

def main():
    parser = argparse.ArgumentParser(description='plot a kicad schema file.')
    parser.add_argument('--input', dest='input', required=True,
                        help='the input filename.')
    parser.add_argument('--output', dest='output', required=True,
                        help='the output filename.')
    parser.add_argument('--border', dest='border', action='store_true', required=False,
                        help='draw the border.')
    args = parser.parse_args()

    plot = nl.SchemaPlot(args.output, 297, 210, 600)
    with nl.schema(args.input, plot) as _:
        pass

if __name__ == "__main__":
    main()
