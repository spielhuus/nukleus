from typing import List, cast

from .AbstractParser import AbstractParser
from .ModelBase import TitleBlock
from .ModelSchema import (Bus, BusEntry, GlobalLabel, GraphicalLine,
                    GraphicalText, HierarchicalLabel, HierarchicalSheet,
                    HierarchicalSheetInstance, Junction, LibrarySymbol,
                    LocalLabel, NoConnect, SchemaElement, Symbol,
                    SymbolInstance, Wire)
from .Library import Library

class Schema(AbstractParser):
    """Kicad schema implementation."""

    def __init__(self, library_path: List[str]|None = None,
                 child: AbstractParser | None=None) -> None:
        super().__init__(child)
        self._next = child
        self.library = Library(library_path)
        self.version: str = ""
        self.generator: str = ""
        self.uuid: str = ""
        self.paper: str = ""
        self.title_block: TitleBlock|None = None
        self.elements: List[SchemaElement] = []
        self.libraries: List[LibrarySymbol] = []
        self.sheet_instance: List[HierarchicalSheetInstance] = []
        self.symbol_instance: List[SymbolInstance] = []

    def __contains__(self, name) -> bool:
        for symbol in self.elements:
            if isinstance(symbol, Symbol):
                if(symbol.has_property("Reference") and
                   symbol.property('Reference').value == name):
                    return True
        return False

    def __getattr__(self, name) -> List[Symbol] | Symbol:
        syms: List[Symbol] = []
        for symbol in self.elements:
            if isinstance(symbol, Symbol):
                if(symbol.has_property("Reference") and
                   symbol.property('Reference').value == name):
                    syms.append(symbol)
        return syms

    def append(self, element: SchemaElement):
        """
        Append an element to the schema.

        :param element: Element to append.
        :type element: E
        """
        if isinstance(element, LibrarySymbol):
            self.libraries.append(element)
        else:
            self.elements.append(element)

    def start(self, version: str, generator: str):
        self.version = version
        self.generator = generator
        super().start(version, generator)

    def visitIdentifier(self, identifier: str):
        """The schema identifier"""
        self.uuid = identifier
        super().visitIdentifier(identifier)

    def visitPaper(self, paper: str):
        """The schema paper size."""
        self.paper = paper
        super().visitPaper(paper)

    def visitTitleBlock(self, title_block: TitleBlock):
        """The schema title block."""
        self.title_block = title_block
        super().visitTitleBlock(title_block)

    def visitWire(self, wire: Wire):
        self.elements.append(wire)
        super().visitWire(wire)

    def visitJunction(self, junction: Junction):
        self.elements.append(junction)
        super().visitJunction(junction)

    def visitNoConnect(self, no_connect: NoConnect):
        self.elements.append(no_connect)
        super().visitNoConnect(no_connect)

    def visitLocalLabel(self, local_label: LocalLabel):
        self.elements.append(local_label)
        super().visitLocalLabel(local_label)

    def visitGlobalLabel(self, global_label: GlobalLabel):
        self.elements.append(global_label)
        super().visitGlobalLabel(global_label)

    def visitGraphicalLine(self, graphical_line: GraphicalLine):
        self.elements.append(graphical_line)
        super().visitGraphicalLine(graphical_line)

    def visitGraphicalText(self, graphical_text: GraphicalText):
        self.elements.append(graphical_text)
        super().visitGraphicalText(graphical_text)

    def visitHierarchicalSheet(self, hierarchical_sheet: HierarchicalSheet):
        self.elements.append(hierarchical_sheet)
        super().visitHierarchicalSheet(hierarchical_sheet)

    def visitHierarchicalLabel(self, hierarchical_label: HierarchicalLabel):
        self.elements.append(hierarchical_label)
        super().visitHierarchicalLabel(hierarchical_label)

    def visitSymbol(self, symbol: Symbol):
        self.elements.append(symbol)
        super().visitSymbol(symbol)

    def visitLibrarySymbol(self, symbol: LibrarySymbol):
        self.libraries.append(symbol)
        super().visitLibrarySymbol(symbol)

    def visitSheetInstance(self, sheet: HierarchicalSheetInstance):
        self.sheet_instance.append(sheet)
        super().visitSheetInstance(sheet)

    def visitSymbolInstance(self, symbol: SymbolInstance):
        self.symbol_instance.append(symbol)
        super().visitSymbolInstance(symbol)

    def visitBus(self, bus: Bus):
        self.elements.append(bus)
        super().visitBus(bus)

    def visitBusEntry(self, bus_entry: BusEntry):
        self.elements.append(bus_entry)
        super().visitBusEntry(bus_entry)

    def produce(self, parser: AbstractParser):
        parser.start(self.version, self.generator)
        parser.visitIdentifier(self.uuid)
        parser.visitPaper(self.paper)
        if self.title_block:
            parser.visitTitleBlock(self.title_block)

        parser.startLibrarySymbols()
        for element in self.libraries:
            parser.visitLibrarySymbol(element)
        parser.endLibrarySymbols()

        for schema_element in self.elements:
            if isinstance(schema_element, Junction):
                parser.visitJunction(schema_element)
            elif isinstance(schema_element, NoConnect):
                parser.visitNoConnect(cast(NoConnect, schema_element))
            elif isinstance(schema_element, BusEntry):
                parser.visitBusEntry(cast(BusEntry, schema_element))
            elif isinstance(schema_element, Wire):
                parser.visitWire(cast(Wire, schema_element))
            elif isinstance(schema_element, Bus):
                parser.visitBus(cast(Bus, schema_element))
            elif isinstance(schema_element, GraphicalLine):
                parser.visitGraphicalLine(cast(GraphicalLine, schema_element))
            elif isinstance(schema_element, GraphicalText):
                parser.visitGraphicalText(cast(GraphicalText, schema_element))
            elif isinstance(schema_element, LocalLabel):
                parser.visitLocalLabel(cast(LocalLabel, schema_element))
            elif isinstance(schema_element, GlobalLabel):
                parser.visitGlobalLabel(cast(GlobalLabel, schema_element))
            elif isinstance(schema_element, HierarchicalLabel):
                parser.visitHierarchicalLabel(cast(HierarchicalLabel, schema_element))
            elif isinstance(schema_element, Symbol):
                parser.visitSymbol(cast(Symbol, schema_element))
            elif isinstance(schema_element, HierarchicalSheet):
                parser.visitHierarchicalSheet(cast(HierarchicalSheet, schema_element))
            else:
                raise ValueError(f'unknown SchemaElement: {type(schema_element)}')

        parser.startSheetInstances()
        for sheet in self.sheet_instance:
            parser.visitSheetInstance(cast(HierarchicalSheetInstance, sheet))
        parser.endSheetInstances()
        parser.startSymbolInstances()
        for symbol in self.symbol_instance:
            parser.visitSymbolInstance(cast(SymbolInstance, symbol))
        parser.endSymbolInstances()
        parser.end()
