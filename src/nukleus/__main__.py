import argparse
import logging
import os
import shutil
import sys
from json import load

from nukleus import Layer, bom, load_pcb, load_schema, pdf, plot


def main() -> int:
    """Echo the input arguments to standard output"""
    parser = argparse.ArgumentParser(
        description='Nukleus electronic processing.')
    parser.add_argument('--bom', dest='action', action='append_const', const='bom',
                        help='Output the BOM as JSON')
    parser.add_argument('--plot', dest='action', action='append_const', const='plot',
                        help='Plot the Schema')
    parser.add_argument('--pcb', dest='action', action='append_const', const='pcb',
                        help='Plot the Board')
    parser.add_argument('--input', dest='input',
                        help='The input filename.')
    parser.add_argument('--output', dest='output',
                        help='The output filename.')

    # initialize the logger
    logging.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=logging.INFO)
    logging.getLogger().setLevel(logging.INFO)

    args = parser.parse_args()
    print(args)

    schema = None
    pcb = None
    if args.input.endswith('.kicad_sch'):
        schema = load_schema(args.input)
    if args.input.endswith('.kicad_pcb'):
        pcb = load_pcb(args.input)

    for action in args.action:
        if action == 'bom':
            bom_res = bom(schema)
            print(bom_res)
        if action == 'plot':
            if args.output is None:
                print('Output file is required for plot schematic.')
                sys.exit(1)
            plot(schema, args.output, border=True)
        if action == 'pcb':
            if args.output is None:
                print('Output file is required for plot PCB.')
                sys.exit(1)
            if not pcb:
                print('PCB input file is not set.')
                sys.exit(1)

            layer_names = ('F.Cu', 'B.Cu', 'In1.Cu', 'In2.Cu', 'In3.Cu', 'In4.Cu',
                           'In5.Cu', 'In6.Cu', 'F.SilkS', 'B.SilkS', 'F.Mask',
                           'B.Mask', 'Edge.Cuts')
            layers = []
            for layer in layer_names:
                layers.append(Layer.from_name(pcb, layer))
            tmp_dir = os.path.join(os.getcwd(), 'temp')
            pdf(pcb, args.output, layers, tmp_dir)
            shutil.rmtree(tmp_dir)

    return 0


if __name__ == '__main__':
    sys.exit(main())
