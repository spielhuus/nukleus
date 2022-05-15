from os import wait
from typing import IO, List

from nukleus.AbstractParser import AbstractParser
from nukleus.draw.Draw import Draw

from .Schema import Schema
from .SexpParser import SexpNode, load_tree
from .SexpWriter import SexpWriter
from .ParserVisitor import ParserVisitor
from .SchemaPlot import SchemaPlot
from .plot.PlotSvgWrite import PlotSvgWrite
from .Circuit import Circuit
from .Netlist import Netlist
from .spice import *
from .SpiceModel import load_spice_models
from .SchemaDraw import SchemaDraw
from .Registry import Registry
from .transform import get_pins as pins

def get_spice_path():
    return Registry().spice_path

def set_spice_path(paths: List[str]):
    Registry().spice_path = paths

def get_library_path():
    return Registry().library_path

def set_library_path(paths: List[str]):
    Registry().library_path = paths


class schema():
    def __init__(self, path: str, consumer: AbstractParser, encoding: str='utf-8') -> None:
        self.path = path
        self.encoding = encoding
        self.tree: SexpNode|None = None
        self.consumer = consumer

    def __enter__(self):
        with open(self.path, 'r', encoding=self.encoding) as filep:
            self.tree = load_tree(filep.read())
            parser = ParserVisitor(self.consumer)
            parser.visit(self.tree)
            return self.consumer

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass

class circuit():
    def __init__(self, netlist: Netlist) -> None:
        self.netlist = netlist
        self._circuit = Circuit()

    def __enter__(self):
        self.netlist.spice(self._circuit)
        return self._circuit

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass

class spice():
    def __init__(self, cir: Circuit) -> None:
        self.circuit = cir
        self._spice = ngspice()

    def __enter__(self) -> ngspice:
        self._spice.circuit(str(self.circuit))
        return self._spice

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass

class draw():
    def __init__(self, child: AbstractParser) -> None:
        self.child = child
        self._draw = SchemaDraw(Registry().library_path)

    def __enter__(self) -> SchemaDraw:
        return self._draw

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._draw.produce(self.child)
