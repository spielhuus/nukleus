from typing import Dict, List, Type, cast

from .AbstractParser import AbstractParser
from .ModelBase import TitleBlock
from .ModelSchema import (BaseElement, Bus, BusEntry, GlobalLabel, GraphicalLine,
                    GraphicalText, HierarchicalLabel, HierarchicalSheet,
                    HierarchicalSheetInstance, Junction, LibrarySymbol,
                    LocalLabel, NoConnect, SchemaElement, Symbol,
                    SymbolInstance, Wire)
from .Library import Library

class Schema(AbstractParser):
    """Kicad schema implementation."""

    def __init__(self, library_path: List[str]|None = None) -> None:
        self.library = Library(library_path)
        self.version: str = ""
        self.generator: str = ""
        self.uuid: str = ""
        self.paper: str = ""
        self.title_block: TitleBlock = TitleBlock()

        self.content: Dict[Type, List[BaseElement]] = {
            Wire: [],
            Junction: [],
            NoConnect: [],
            LocalLabel: [],
            GlobalLabel: [],
            GraphicalLine: [],
            GraphicalText: [],
            HierarchicalSheet: [],
            HierarchicalLabel: [],
            Symbol: [],
            LibrarySymbol: [],
            SymbolInstance: [],
            HierarchicalSheetInstance: [],
            Bus: [],
            BusEntry: [],
        }

    def __contains__(self, name) -> bool:
        for symbol in self.content[Symbol]:
            if cast(Symbol, symbol).has_property("Reference"):
                if cast(Symbol, symbol).property('Reference').value == name:
                    return True
        return False

    def __getattr__(self, name) -> List[Symbol] | Symbol:
        syms: List[Symbol] = []
        for symbol in self.content[Symbol]:
            if cast(Symbol, symbol).has_property("Reference"):
                if cast(Symbol, symbol).property('Reference').value == name:
                    syms.append(cast(Symbol, symbol))
        return syms

    def append(self, element: SchemaElement):
        """
        Append an element to the schema.

        :param element: Element to append.
        :type element: E
        """
        self.content[type(element)].append(element)

    def start(self, version: str, identifier: str, generator: str,
              paper: str, title_block: TitleBlock | None):
        self.version = version
        self.uuid = identifier
        self.generator = generator
        self.paper = paper
        if title_block:
            self.title_block = title_block

    def end(self):
        pass

    def visitWire(self, wire: Wire):
        self.content[Wire].append(wire)

    def visitJunction(self, junction: Junction):
        self.content[Junction].append(junction)

    def visitNoConnect(self, no_connect: NoConnect):
        self.content[NoConnect].append(no_connect)

    def visitLocalLabel(self, local_label: LocalLabel):
        self.content[LocalLabel].append(local_label)

    def visitGlobalLabel(self, global_label: GlobalLabel):
        self.content[GlobalLabel].append(global_label)

    def visitGraphicalLine(self, graphical_line: GraphicalLine):
        self.content[GraphicalLine].append(graphical_line)

    def visitGraphicalText(self, graphical_text: GraphicalText):
        self.content[GraphicalText].append(graphical_text)

    def visitHierarchicalSheet(self, hierarchical_sheet: HierarchicalSheet):
        self.content[HierarchicalSheet].append(hierarchical_sheet)

    def visitHierarchicalLabel(self, hierarchical_label: HierarchicalLabel):
        self.content[HierarchicalLabel].append(hierarchical_label)

    def visitSymbol(self, symbol: Symbol):
        self.content[Symbol].append(symbol)

    def visitLibrarySymbol(self, symbol: LibrarySymbol):
        self.content[LibrarySymbol].append(symbol)

    def visitSheetInstance(self, sheet: HierarchicalSheetInstance):
        self.content[HierarchicalSheetInstance].append(sheet)

    def visitSymbolInstance(self, symbol: SymbolInstance):
        self.content[SymbolInstance].append(symbol)

    def visitBus(self, bus: Bus):
        self.content[Bus].append(bus)

    def visitBusEntry(self, bus_entry: BusEntry):
        self.content[BusEntry].append(bus_entry)

    def produce(self, parser: AbstractParser):
        assert self.title_block, "Title block is not set."
        parser.start(self.version, self.uuid, self.generator,
                     self.paper, self.title_block)
        parser.startLibrarySymbols()
        for element in self.content[LibrarySymbol]:
            parser.visitLibrarySymbol(cast(LibrarySymbol, element))
        parser.endLibrarySymbols()
        for element in self.content[Junction]:
            parser.visitJunction(cast(Junction, element))
        for element in self.content[NoConnect]:
            parser.visitNoConnect(cast(NoConnect, element))
        for element in self.content[Wire]:
            parser.visitWire(cast(Wire, element))
        for element in self.content[LocalLabel]:
            parser.visitLocalLabel(cast(LocalLabel, element))
        for element in self.content[GlobalLabel]:
            parser.visitGlobalLabel(cast(GlobalLabel, element))
        for element in self.content[Symbol]:
            parser.visitSymbol(cast(Symbol, element))
        parser.startSheetInstances()
        for element in self.content[HierarchicalSheetInstance]:
            parser.visitSheetInstance(cast(HierarchicalSheetInstance, element))
        parser.endSheetInstances()
        parser.startSymbolInstances()
        for element in self.content[SymbolInstance]:
            parser.visitSymbolInstance(cast(SymbolInstance, element))
        parser.endSymbolInstances()
        parser.end()
