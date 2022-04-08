from typing import List

from . import draw, model, spice
from .Bom import bom
from .Circuit import Circuit
from .Library import Library
from .ParserV6 import ParserV6
from .PcbUtils import PCB, Layer
from .Plot import plot
from .PlotPcb import pcb, pdf
from .Reports import report_parser
from .Schema import Schema
from .Netlist import Netlist
from .SpiceModel import load_spice_models
from .PCB import PCB

# SYMBOL_SEARCH_PATH_POSIX = [
#    '/usr/share/kicad/symbols',
#    '/usr/local/share/kicad/symbols'
# ]
#SYMBOL_LIBRARIES = []
#
# if os.name == 'posix':
#    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!search libraries")
#    for search_path in SYMBOL_SEARCH_PATH_POSIX:
#        if os.path.exists(search_path):
#            print(f"add library path: {search_path}")
#            SYMBOL_LIBRARIES.append(search_path)
# else:
#    sys.exit(f'OS {os.name} not supported!')


#from .Spice import Spice

#def load_pcb(filename: str):
#    return PCB(filename)

def load_schema(filename: str):
    schema = Schema()
    parser = ParserV6()
    parser.schema(schema, filename)
    return schema

def load_pcb(filename: str):
    pcb = PCB()
    parser = ParserV6()
    parser.pcb(pcb, filename)
    return pcb

def spice_path(paths: List[str]):
    return load_spice_models(paths)
