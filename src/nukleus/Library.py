from __future__ import annotations
from functools import lru_cache
import os
from copy import deepcopy
from typing import cast, Dict, List
from .AbstractParser import AbstractParser
from .ModelSchema import LibrarySymbol
from .ParserVisitor import ParserVisitor
from .SexpParser import load_tree, SexpNode

class LibrarySymbolNotFound(Exception):
    """Library can not be found."""


class LibrarySymbolFromat(Exception):
    """When the library symbol name has wrong format."""

class _LibraryParser(ParserVisitor):
#   def __init__(self, consumer: AbstractParser):
#       super().__init__(consumer)
    def node(self, name: str, sexp: SexpNode) -> None:
        if name == 'symbol':
            lib_symbol = ParserVisitor._get_library_symbol(cast(SexpNode, sexp))
            self.consumer.visitLibrarySymbol(lib_symbol)

class _LibraryVisitor(AbstractParser):
    def __init__(self):
        super().__init__(None)
        self.libraries: List[LibrarySymbol] = []

    def visitLibrarySymbol(self, symbol: LibrarySymbol):
        self.libraries.append(symbol)


class Library(AbstractParser):
    """Handle the symbol libraries."""

    def __init__(self, paths: List[str] | None = None):
        self.paths = [] if paths is None else paths
        self.symbols: Dict[str, List[LibrarySymbol]] = {}

    def search(self, pattern):
        pass

    @lru_cache
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
                self.symbols[prefix] = self._load(filename, self)
                return True
        raise LibrarySymbolNotFound(
            "Symbol prefix not found", prefix, self.paths)


    @classmethod
    @lru_cache
    def _load(cls, filename, consumer) -> List[LibrarySymbol]:
        with open(filename, 'r', encoding='utf-8') as file:
            tree = load_tree(file.read())
            visitor = _LibraryVisitor()
            parser = _LibraryParser(visitor)
            parser.visit(tree)
            return visitor.libraries
