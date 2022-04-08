import sys
import argparse

sys.path.append('src')
sys.path.append('../src')

from nukleus.PlotPcbSvg import plot

import nukleus

def main():
    parser = argparse.ArgumentParser(description='plot a kicad pcb file.')
    parser.add_argument('--input', dest='input', required=True,
                        help='the input filename.')
    parser.add_argument('--output', dest='output', required=True,
                        help='the output filename.')
    parser.add_argument('--border', dest='border', action='store_true', required=False,
                        help='draw the border.')
    args = parser.parse_args()

    pcb = nukleus.load_pcb(args.input)
    plot(pcb, args.output, border=args.border)

if __name__ == "__main__":
    main()
