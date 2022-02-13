from os import register_at_fork
from typing import Dict, List

from nukleus import Library, Schema
from nukleus.model import Symbol

from .DrawElement import DrawElement


class Draw(Schema):
    def __init__(self, library_path: List[str] = []):
        super().__init__()
        self.unit: float = 2.54
        #self.orientation = ORIENTATION['left']
        #self.element_stack = []
        self.last_pos = (20, 20)
        #self.last_attr_element = None
        self.library = Library(library_path)
        self.symbols: Dict[str, DrawElement] = {}

    def add(self, element: DrawElement):
        last_draw, symbol, self.last_pos = element._get(
            self.library, self.last_pos, self.unit)
        if isinstance(symbol, Symbol):
            self.symbols[symbol.property("Reference").value] = last_draw
            if not self.has_symbol(last_draw.library_symbol.identifier):
                self.append(last_draw.library_symbol)
        self.append(symbol)
        return self

#    def pin(self, ref, unit=1, pin='1'):
#        units = getattr(self, ref)
#        for _unit in units:
#            if _unit.unit == unit:
#                pins = _unit.getPins()
#                for _pin in pins:
#                    if _pin.number[0] == pin:
#                        return _unit._pos(_pin._pos())
#
#        raise Exception('Pin not found', ref, unit, pin)
