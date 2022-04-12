from typing import Dict, List

from ..Library import Library
from ..Schema import Schema
from .. import model

from .DrawElement import DrawElement


class Draw(Schema):
    """ Drawing to add symbols, wires and such. """

    def __init__(self, library_path: List[str]|None = None):
        super().__init__()
        self.unit: float = 2.54
        self.last_pos = (20, 20)
        self.library = Library(library_path)
        self.symbols: Dict[str, DrawElement] = {}

    def add(self, element: DrawElement):
        """ add an element to this drawing """
        last_draw, symbol, self.last_pos, extra_elements = element._get(
            self.library, self.last_pos, self.unit)
        if isinstance(symbol, model.Symbol):
            self.symbols[symbol.property('Reference').value] = last_draw
            if not self.has_symbol(last_draw.library_symbol.identifier):
                self.append(last_draw.library_symbol)
        self.append(symbol)

        if extra_elements:
            for extra_element in extra_elements:
                self.add(extra_element)
        return self
