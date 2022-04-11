import sys
import argparse

sys.path.append('src')
sys.path.append('../src')

import nukleus

def main():
    parser = argparse.ArgumentParser(description='plot a kicad schema file.')
    parser.add_argument('--input', dest='input', required=True,
                        help='the input filename.')
    parser.add_argument('--output', dest='output', required=True,
                        help='the output filename.')
    parser.add_argument('--border', dest='border', action='store_true', required=False,
                        help='draw the border.')
    args = parser.parse_args()

    schema = nukleus.load_schema(args.input)

    nukleus.plot(schema, args.output, border=args.border)

if __name__ == "__main__":
    main()
