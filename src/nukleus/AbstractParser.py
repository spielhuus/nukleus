from __future__ import annotations

from .ModelBase import TitleBlock
from .ModelPcb import (Footprint, Net, PcbGeneral, PcbGraphicalLine, PcbLayer,
                       PcbSetup, TrackSegment, TrackVia)
from .ModelSchema import (Bus, BusEntry, GlobalLabel, GraphicalLine,
                          GraphicalText, HierarchicalLabel, HierarchicalSheet,
                          HierarchicalSheetInstance, Junction, LibrarySymbol,
                          LocalLabel, NoConnect, Symbol, SymbolInstance, Wire)


class AbstractParser():
    """
    Abstract class for parsing data.
    """
    def __init__(self, child: AbstractParser | None) -> None:
        self._next = child

    def start(self, version: str, generator: str):
        """
        Start diagram parsing

        :param version str: The version token attribute defines the
                            schematic version using the YYYYMMDD date
                            format.
        :param generator str: The generator token attribute defines the
                              program used to write the file.
        """
        if self._next:
            self._next.start(version, generator)

    def visitIdentifier(self, identifier: str):
        """The schema identifier"""
        if self._next:
            self._next.visitIdentifier(identifier)

    def visitPaper(self, paper: str):
        """The schema paper size."""
        if self._next:
            self._next.visitPaper(paper)

    def visitTitleBlock(self, title_block: TitleBlock):
        """The schema title block."""
        if self._next:
            self._next.visitTitleBlock(title_block)

    def end(self):
        """End diagram parsing"""
        if self._next:
            self._next.end()

    def startSheetInstances(self):
        """Start parsing sheet instances"""
        if self._next:
            self._next.startSheetInstances()

    def endSheetInstances(self):
        """End parsing sheet instances"""
        if self._next:
            self._next.endSheetInstances()

    def startSymbolInstances(self):
        """Start parsing symbol instances"""
        if self._next:
            self._next.startSymbolInstances()

    def endSymbolInstances(self):
        """End parsing symbol instances"""
        if self._next:
            self._next.endSymbolInstances()

    def visitBus(self, bus: Bus):
        """Bus Symbol"""
        if self._next:
            self._next.visitBus(bus)

    def visitBusEntry(self, bus_entry: BusEntry):
        """BusEntry Symbol"""
        if self._next:
            self._next.visitBusEntry(bus_entry)

    def visitWire(self, wire: Wire):
        """Wire Symbol"""
        if self._next:
            self._next.visitWire(wire)

    def visitJunction(self, junction: Junction):
        """Junction Symbol"""
        if self._next:
            self._next.visitJunction(junction)

    def visitNoConnect(self, no_connect: NoConnect):
        """No Connect Symbol"""
        if self._next:
            self._next.visitNoConnect(no_connect)

    def visitLocalLabel(self, local_label: LocalLabel):
        """Local Label"""
        if self._next:
            self._next.visitLocalLabel(local_label)

    def visitGlobalLabel(self, global_label: GlobalLabel):
        """Global Label"""
        if self._next:
            self._next.visitGlobalLabel(global_label)

    def visitGraphicalLine(self, graphical_line: GraphicalLine):
        """Graphical Line"""
        if self._next:
            self._next.visitGraphicalLine(graphical_line)

    def visitGraphicalText(self, graphical_text: GraphicalText):
        """Graphical Text"""
        if self._next:
            self._next.visitGraphicalText(graphical_text)

    def visitHierarchicalSheet(self, hierarchical_sheet: HierarchicalSheet):
        """Hirarchical Sheet"""
        if self._next:
            self._next.visitHierarchicalSheet(hierarchical_sheet)

    def visitHierarchicalLabel(self, hierarchical_label: HierarchicalLabel):
        """Hirarchical Sheet"""
        if self._next:
            self._next.visitHierarchicalLabel(hierarchical_label)

    def visitSymbol(self, symbol: Symbol):
        """Symbol"""
        if self._next:
            self._next.visitSymbol(symbol)

    def startLibrarySymbols(self):
        """Start parsing library symbols"""
        if self._next:
            self._next.startLibrarySymbols()

    def endLibrarySymbols(self):
        """End parsing library symbols"""
        if self._next:
            self._next.endLibrarySymbols()

    def visitLibrarySymbol(self, symbol: LibrarySymbol):
        """Library Symbol"""
        if self._next:
            self._next.visitLibrarySymbol(symbol)

    def visitSheetInstance(self, sheet: HierarchicalSheetInstance):
        """Sheet Instance"""
        if self._next:
            self._next.visitSheetInstance(sheet)

    def visitSymbolInstance(self, symbol: SymbolInstance):
        """Symbol Instance"""
        if self._next:
            self._next.visitSymbolInstance(symbol)

    def visitPcbGeneral(self, general: PcbGeneral):
        """General Instance"""
        if self._next:
            self._next.visitPcbGeneral(general)

    def visitPcbSetup(self, setup: PcbSetup):
        """PCB setup Instance"""
        if self._next:
            self._next.visitPcbSetup(setup)

    def visitFootprint(self, footprint: Footprint):
        """Footprint Instance"""
        if self._next:
            self._next.visitFootprint(footprint)

    def startLayers(self):
        """Start Layers Instance"""
        if self._next:
            self._next.startLayers()

    def endLayers(self):
        """Start Layers Instance"""
        if self._next:
            self._next.endLayers()

    def visitLayer(self, layer: PcbLayer):
        """Layer Instance"""
        if self._next:
            self._next.visitLayer(layer)

    def visitSegment(self, segment: TrackSegment):
        """Track segment instance"""
        if self._next:
            self._next.visitSegment(segment)

    def visitVia(self, via: TrackVia):
        """Track via instance"""
        if self._next:
            self._next.visitVia(via)

    def visitNet(self, net: Net):
        """Net instance"""
        if self._next:
            self._next.visitNet(net)

    def visitPcbGraphicalLine(self, graphical_line: PcbGraphicalLine):
        """PCB Graphical Line instance"""
        if self._next:
            self._next.visitPcbGraphicalLine(graphical_line)
