from typing import Dict, List

from .Schema import Schema
from .ModelSchema import Symbol
from .draw.DrawElement import DrawElement
from .Library import Library

class SchemaDraw(Schema):
    """Kicad schema implementation."""

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
        if isinstance(symbol, Symbol):
            self.symbols[symbol.property('Reference').value] = last_draw
            if not last_draw.library_symbol.identifier in self:
                self.append(last_draw.library_symbol)
        self.append(symbol)

        if extra_elements:
            for extra_element in extra_elements:
                self.add(extra_element)

        return self
