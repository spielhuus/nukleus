from typing import List, cast

import logging

from nukleus.model.BusEntry import BusEntry

from .model.Bus import Bus
from .model.Image import Image
from .model.GlobalLabel import GlobalLabel
from .model.GraphicalText import GraphicalText
from .model.GraphicalLine import GraphicalLine
from .model.HierarchicalLabel import HierarchicalLabel
from .model.HierarchicalSheet import HierarchicalSheet
from .model.HierarchicalSheetInstance import HierarchicalSheetInstance
from .model.Junction import Junction
from .model.LibrarySymbol import LibrarySymbol
from .model.LocalLabel import LocalLabel
from .model.NoConnect import NoConnect
from .model.Symbol import Symbol
from .model.SymbolInstance import SymbolInstance
from .model.Wire import Wire
from .Schema import Schema
from .SexpParser import load_tree
from .SexpParser import SEXP_T

logger = logging.getLogger(__name__)

class _ParserV6Factory:
    def __init__(self):
        self.parsers = {
            'junction': Junction,
            'no_connect': NoConnect,
            'bus_entry': BusEntry,
            'wire': Wire,
            'bus': Bus,
            'image': Image,
            'text': GraphicalText,
            'label': LocalLabel,
            'global_label': GlobalLabel,
            'hierarchical_label': HierarchicalLabel,
            'symbol': Symbol,
            'sheet': HierarchicalSheet,
            'sheet_istances': HierarchicalSheetInstance,
            'symbol_instances': SymbolInstance,
            'polyline': GraphicalLine
        }

    def parse(self, token: SEXP_T):
        parser_impl = self.parsers.get(str(token[0]))
        if parser_impl:
            return parser_impl.parse(token)
        raise ValueError(f"unknown schema element {token}")

class ParserV6():
    """Parse the Kicad V6 Shema"""

    def __init__(self) -> None:
        """
        Create a new SchemaV6 Parser.

        :return: initialized parser.
        :rtype: SchemaV6
        """
        self.library_symbols: List[LibrarySymbol] = []

    @classmethod
    def _title_block(cls, schema: Schema, sexp: SEXP_T) -> None:
        for token in sexp[1:]:
            if token[0] == 'title':
                schema.title = token[1]
            elif token[0] == 'date':
                schema.date = token[1]
            elif token[0] == 'company':
                schema.company = token[1]
            elif token[0] == 'rev':
                schema.rev = token[1]
            elif token[0] == 'comment':
                index = int(token[1])
                schema.comment[index] = token[2]
            else:
                raise ValueError(f"unknown title block element {token}")

    def schema(self, schema: Schema, file: str) -> None:
        """
        Open a schema from the filesystem.

        :param file: filename
        :type file: str
        """
        with open(file, 'r', encoding="UTF-8") as handle:
            parsed = load_tree(handle.read())
            factory = _ParserV6Factory()
            for item in parsed[1:]:
                if item[0] == 'version':
                    schema.version = str(item[1])
                elif item[0] == 'generator':
                    schema.generator = item[1]
                elif item[0] == 'uuid':
                    schema.uuid = item[1]
                elif item[0] == 'paper':
                    schema.paper = item[1]
                elif item[0] == 'title_block':
                    self._title_block(schema, cast(SEXP_T, item))
                elif item[0] == 'lib_symbols':
                    for symbol in item[1:]:
                        schema.append(LibrarySymbol.parse(cast(SEXP_T, symbol)))
                elif item[0] == 'symbol_instances':
                    for symbol in item[1:]:
                        schema.append(SymbolInstance.parse(symbol))
                elif item[0] == 'sheet_instances':
                    for path in item[1:]:
                        schema.append(
                            HierarchicalSheetInstance.parse(path))
                else:
                    element = factory.parse(cast(SEXP_T, item))
                    if isinstance(element, Symbol):
                        element.library_symbol = schema.getSymbol(
                            element.library_identifier, LibrarySymbol)
                    schema.append(element)

    @classmethod
    def libraries(cls, target, file: str) -> None:
        """
        Open a schema from the filesystem.

        :param file: filename
        :type file: str
        """
        with open(file, 'r', encoding="UTF-8") as handle:
            parsed = load_tree(handle.read())
            for item in parsed[1:]:
                if item[0] == 'symbol':
                    target.append(LibrarySymbol.parse(cast(SEXP_T, item)))
                elif item[0] == 'generator':
                    if item[1] != 'kicad_symbol_editor':
                        logger.warning('generator is %s', item[1])
                elif item[0] != 'version':
                    raise ValueError(f"unknown library element {item}")

    @classmethod
    def pcb(cls, target, file: str) -> None:
        """
        Open a PCB from the filesystem.

        :param file: filename
        :type file: str
        """
        with open(file, 'r', encoding="UTF-8") as handle:
            parsed = load_tree(handle.read())
            for item in parsed[1:]:
                if item[0] == 'symbol':
                    target.append(LibrarySymbol.parse(cast(SEXP_T, item)))
                elif item[0] == 'generator':
                    if item[1] != 'kicad_symbol_editor':
                        logger.warning('generator is %s', item[1])
                elif item[0] != 'version':
                    raise ValueError(f"unknown library element {item}")
