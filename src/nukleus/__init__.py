from typing import List

import os
import sys
import json
import shutil

from . import draw, model, spice
from .Circuit import Circuit
from .Library import Library
from .ParserV6 import ParserV6
from .Plot import plot
from .Schema import Schema
from .Spice import netlist, schema_to_spice
from .SpiceModel import load_spice_models
from .Bom import bom
from .Reports import report_parser
from .ERC import erc

#SYMBOL_SEARCH_PATH_POSIX = [
#    '/usr/share/kicad/symbols',
#    '/usr/local/share/kicad/symbols'
#]
#SYMBOL_LIBRARIES = []
#
#if os.name == 'posix':
#    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!search libraries")
#    for search_path in SYMBOL_SEARCH_PATH_POSIX:
#        if os.path.exists(search_path):
#            print(f"add library path: {search_path}")
#            SYMBOL_LIBRARIES.append(search_path)
#else:
#    sys.exit(f'OS {os.name} not supported!')


#from .Spice import Spice


def load_schema(filename: str):
    schema = Schema()
    parser = ParserV6()
    parser.schema(schema, filename)
    return schema

def spice_path(paths: List[str]):
    return load_spice_models(paths)
