from __future__ import annotations

import os
from copy import deepcopy
from typing import List

from .model import LibrarySymbol
from .ParserV6 import ParserV6


class LibrarySymbolNotFound(Exception):
    """Library can not be found."""


class LibrarySymbolFromat(Exception):
    """When the library symbol name has wrong format."""


class Library():
    """Handle the symbol libraries."""

    def __init__(self, paths: List[str] | None = None):
        self.paths = [] if paths is None else paths
        self.symbols = {}

    def search(self, pattern):
        pass

    # @lru_cache
    def get(self, name) -> LibrarySymbol:
        """
        Load a library symbol.

        :param name str: Name of the library symbol.
        :rtype LibrarySymbol: The Symbol instance.
        :raises LibrarySymbolNotFound: Library symbol not found.
        """
        if not ':' in name:
            raise LibrarySymbolFromat(
                'The library symbol format is GROUP:NAME')

        prefix, suffix = name.split(':')
        if not prefix in self.symbols:
            self._load_symbols(prefix)

        for symbol in self.symbols[prefix]:
            if symbol.identifier == suffix:
                if symbol.extends not in ('', 'power'):
                    parent_symbol = self.get(
                        f'{prefix}:{symbol.extends}')
                    symbol.units = parent_symbol.units
                return deepcopy(symbol)

        raise LibrarySymbolNotFound("Symbol not found", name, self.paths)

    def _load_symbols(self, prefix) -> bool:
        # load the symbols
        for path in self.paths:
            filename = os.path.join(path, f'{prefix}.kicad_sym')
            if os.path.isfile(filename):
                self.symbols[prefix] = self._load(filename)
                return True
        raise LibrarySymbolNotFound(
            "Symbol prefix not found", prefix, self.paths)

    @classmethod
    def _load(cls, filename):
        parser = ParserV6()
        symbols = []
        parser.libraries(symbols, filename)
        return symbols
