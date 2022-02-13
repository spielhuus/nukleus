
from __future__ import annotations

import os

from .ParserV6 import ParserV6
from .model import LibrarySymbol

class LibrarySymbolNotFound(Exception):
    pass

class Library():
    def __init__(self, paths: List[str] = []):
        self.paths = paths
        self.symbols = {}

    def search(pattern):
        pass

    def get(self, name) -> LibrarySymbol:
        prefix, suffix = name.split(':')
        for path in self.paths:
            filename = os.path.join(path, f'{prefix}.kicad_sym')
            exists = os.path.isfile(filename)
            if exists:
                for symbol in self.load(filename):
                    if symbol.identifier == suffix:
                        if symbol.extends != '' and \
                           symbol.extends != 'power':
                            parent_symbol = self.get(f'{prefix}:{symbol.extends}')
                            symbol.units = parent_symbol.units
                        return symbol

        raise LibrarySymbolNotFound("Symbol not found", name, self.paths)

    def load(self, filename):
        parser = ParserV6()
        print(f"open symbol library: {filename}")
        symbols = []
        parser.libraries(symbols, filename)
        return symbols

