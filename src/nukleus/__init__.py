#from .Spice import Spice
from .Schema import Schema
from .Circuit import Circuit

from .ParserV6 import ParserV6
from .Spice import netlist
from .Plot import Plot
from .Library import Library

from . import spice
from . import model
from . import draw

def load_schema(filename: str):
    schema = Schema()
    parser = ParserV6()
    parser.schema(schema, filename)
    return schema

