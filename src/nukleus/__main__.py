import argparse
import logging
from os import wait
import sys
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('module://matplotlib-backend-kitty')

from rich import print, inspect

import nukleus
from nukleus.AbstractParser import AbstractParser
from nukleus.Bom import Bom
from nukleus.SexpWriter import SexpWriter
from .Registry import Registry
from .plot.PlotMatplotlib import PlotMatplotlib
from .SchemaPlot import SchemaPlot

def main() -> int:
    """Echo the input arguments to standard output"""
    parser = argparse.ArgumentParser(
        description='Nukleus electronic processing.')
    parser.add_argument('--bom', dest='action', action='append_const', const='bom',
                        help='Output the BOM as JSON')
    parser.add_argument('--plot', dest='action', action='append_const', const='plot',
                        help='Plot the Schema')
    parser.add_argument('--dump', dest='action', action='append_const', const='dump',
                        help='Dump the Schema content.')
    parser.add_argument('--pcb', dest='action', action='append_const', const='pcb',
                        help='Plot the Board')
    parser.add_argument('--input', dest='input', required=True,
                        help='The input filename.')
    parser.add_argument('--output', dest='output',
                        help='The output filename.')
    parser.add_argument('--plotter', dest='plotter',
                        help='Select the ploter backend', default='PlotSvgWrite')

    # initialize the logger
    logging.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=logging.INFO)
    logging.getLogger().setLevel(logging.INFO)

    args = parser.parse_args()
    inspect(args)

    action: AbstractParser|None = None
    if 'dump' in args.action:
        sexp = action = SexpWriter(action)

    if 'bom' in args.action:
        bom = action = Bom(True, action)

    if 'plot' in args.action:
        if args.plotter == 'PlotSvgWrite':
            from .plot.PlotSvgWrite import PlotSvgWrite
            Registry().PLOTTER = PlotSvgWrite
            action = SchemaPlot(args.output, 297, 210, 600, child=action)

        if args.plotter == 'PlotMatplotlib':
            from .plot.PlotMatplotlib import PlotMatplotlib
            Registry().PLOTTER = PlotMatplotlib
            schem_fig, schem_ax = plt.subplots(figsize=(8, 6))
            action = SchemaPlot(schem_ax, 297, 210, 600, child=action)

        if args.plotter == 'PlotOpenCV':
            from .plot.PlotOpenCV import PlotOpenCV
            Registry().PLOTTER = PlotOpenCV
            action = SchemaPlot(args.output, 297, 210, 600, child=action)

        if args.plotter == 'PlotCairo':
            from .plot.PlotCairo import PlotCairo
            Registry().PLOTTER = PlotCairo
            action = SchemaPlot(args.output, 297, 210, 600, child=action)

    if args.input.endswith('.kicad_sch'):
        assert action, "No Action Set"
        with nukleus.schema(args.input, action) as _:
            pass
    #if args.input.endswith('.kicad_pcb'):
    #    pcb = load_pcb(args.input)

    if 'dump' in args.action:
        print(str(sexp))

    if 'bom' in args.action:
        print(bom.bom())

    if 'plot' in args.action and args.plotter == 'PlotMatplotlib':
        plt.show()

#        if action == 'pcb':
#            if args.output is None:
#                print('Output file is required for plot PCB.')
#                sys.exit(1)
#            if not pcb:
#                print('PCB input file is not set.')
#                sys.exit(1)
#
#            layer_names = ('F.Cu', 'B.Cu', 'In1.Cu', 'In2.Cu', 'In3.Cu', 'In4.Cu',
#                           'In5.Cu', 'In6.Cu', 'F.SilkS', 'B.SilkS', 'F.Mask',
#                           'B.Mask', 'Edge.Cuts')
#            layers = []
#            for layer in layer_names:
#                layers.append(Layer.from_name(pcb, layer))
#            tmp_dir = os.path.join(os.getcwd(), 'temp')
#            pdf(pcb, args.output, layers, tmp_dir)
#            shutil.rmtree(tmp_dir)

    return 0


if __name__ == '__main__':
    sys.exit(main())
