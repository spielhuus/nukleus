from __future__ import annotations

import os
from typing import List

from .model import LibrarySymbol
from .ParserV6 import ParserV6


class LibrarySymbolNotFound(Exception):
    """Library can not be found."""


class Library():
    """Handle the symbol libraries."""

    def __init__(self, paths: List[str] | None = None):
        self.paths = [] if paths is None else paths
        self.symbols = {}

    def search(self, pattern):
        pass

    def get(self, name) -> LibrarySymbol:
        """
        Load a library symbol.

        :param name str: Name of the library symbol.
        :rtype LibrarySymbol: The Symbol instance.
        :raises LibrarySymbolNotFound: Library symbol not found.
        """
        prefix, suffix = name.split(':')
        for path in self.paths:
            filename = os.path.join(path, f'{prefix}.kicad_sym')
            exists = os.path.isfile(filename)
            if exists:
                for symbol in self._load(filename):
                    if symbol.identifier == suffix:
                        if symbol.extends not in ('', 'power'):
                            parent_symbol = self.get(
                                f'{prefix}:{symbol.extends}')
                            symbol.units = parent_symbol.units
                        return symbol

        raise LibrarySymbolNotFound("Symbol not found", name, self.paths)

    @classmethod
    def _load(cls, filename):
        parser = ParserV6()
        symbols = []
        parser.libraries(symbols, filename)
        return symbols
