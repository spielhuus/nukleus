from typing import List

from .model.GlobalLabel import GlobalLabel
from .model.GraphicalText import GraphicalText
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
    def _title_block(cls, schema, sexp) -> None:
        for token in sexp[1:]:
            match token:
                case ['title', title]:
                    schema.title = title
                case ['date', date]:
                    schema.date = date
                case ['rev', rev]:
                    schema.rev = rev
                case ['comment', '1', comment]:
                    schema.comment_1 = comment
                case ['comment', '2', comment]:
                    schema.comment_2 = comment
                case ['comment', '3', comment]:
                    schema.comment_3 = comment
                case ['comment', '4', comment]:
                    schema.comment_4 = comment
                case _:
                    raise ValueError(f"unknown title block element {token}")

    def schema(self, schema: Schema, file: str) -> None:
        """
        Open a schema from the filesystem.

        :param file: filename
        :type file: str
        """
        with open(file, 'r') as f:
            parsed = load_tree(f.read())
            for item in parsed[1:]:
                match item:
                    case ["version", version]:
                        schema.version = str(version)
                    case ["generator", generator]:
                        schema.generator = generator
                    case ["uuid", uuid]:
                        schema.uuid = uuid
                    case ["paper", paper]:
                        schema.paper = paper
                    case ["title_block", *_]:
                        self._title_block(schema, item)
                    case ["lib_symbols", *symbols]:
                        for symbol in symbols:
                            schema.append(LibrarySymbol.parse(symbol))
                    case ["junction", pos, diameter, *color, uuid]:
                        schema.append(Junction.parse(item))
                    case ["no_connect", pos, uuid]:
                        schema.append(NoConnect.parse(item))
                    case ["bus_entry", pts, size, stroke, uuid]:
                        print(f"bus_entry: {uuid}")
                    case ["wire", pts, stroke, uuid]:
                        schema.append(Wire.parse(item))
                    case ["bus", pts, stroke, uuid]:
                        print(f"bus: {uuid}")
                    case ["image", pos, scale, uuid, data]:
                        print(f"image: {uuid}")
                    case ["image", pos, uuid, data]:
                        print(f"image: {uuid}")
                    case ["polyline", pts, stroke, uuid]:
                        print(f"polyline: {uuid}")
                    case ["text", *_]:
                        schema.append(GraphicalText.parse(item))
                    case ["label", text, pos, effects, uuid]:
                        schema.append(LocalLabel.parse(item))
                    case ["global_label", *_]:
                        schema.append(GlobalLabel.parse(item))
                    case ["hierarchical_label", text, shape, pos, effects, uuid]:
                        print(f"hierarchical_label: {uuid}")
                    case ["symbol", *_]:
                        _symbol = Symbol.parse(item)
                        _symbol.library_symbol = schema.getSymbol(
                            _symbol.library_identifier)
                        schema.append(_symbol)
                    case ["sheet", pos, size, autoplaced, stroke, fill, uuid, sheet_name, file_name, *pins]:
                        print(f"sheet: {uuid}")
                        _xy, _angle = self._pos(pos)
                    case ["sheet", *_]:
                        schema.append(HierarchicalSheet.parse(item))
                    case ["sheet_instances", *paths]:
                        for path in paths:
                            schema.append(
                                HierarchicalSheetInstance.parse(path))
                    case ["symbol_instances", *paths]:
                        for path in paths:
                            schema.append(SymbolInstance.parse(path))
                    case _:
                        raise ValueError(f"unknown schema element {item}")

    def libraries(self, target, file: str) -> None:

        with open(file, 'r') as f:
            parsed = load_tree(f.read())
            for item in parsed[1:]:
                match item:
                    case ["symbol", *_]:
                        target.append(LibrarySymbol.parse(item))
                    case _:
                        print(f"!!! Library {item}")
