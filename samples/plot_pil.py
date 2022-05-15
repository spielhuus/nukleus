import sys
import argparse


sys.path.append('src')
sys.path.append('../src')

from nukleus.SchemaPlot import SchemaPlot
from nukleus.plot.PlotPillow import PlotPillow
from nukleus.KicadSchema import KicadSchema
from nukleus.SexpParser import load_tree
from nukleus.ParserVisitor import ParserVisitor
from nukleus.SexpWriter import SexpWriter

def main():
    parser = argparse.ArgumentParser(description='plot a kicad schema file.')
    parser.add_argument('--input', dest='input', required=True,
                        help='the input filename.')
    parser.add_argument('--output', dest='output', required=True,
                        help='the output filename.')
    parser.add_argument('--border', dest='border', action='store_true', required=False,
                        help='draw the border.')
    args = parser.parse_args()

    #schema = nukleus.load_schema(args.input)
    #nukleus.plot(schema, args.output, border=args.border)
    with open(args.input, 'r') as f:

        #load the schema
        tree = load_tree(f.read())
        schema = KicadSchema()
        parser = ParserVisitor(schema)
        parser.visit(tree)

        #print the schema
        writer = SexpWriter()
        schema.produce(writer)
        writer.write()
        #with open(args.output, 'w') as out:

        plotter = PlotPillow(args.output, 297, 210, 600)
        plot = SchemaPlot(plotter)
        schema.produce(plot)
        plotter.write()

if __name__ == "__main__":
    main()
