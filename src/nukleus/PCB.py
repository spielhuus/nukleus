from typing import Dict, List

from .AbstractParser import AbstractParser
from .ModelBase import BaseElement, TitleBlock
from .ModelPcb import PcbLayer, TrackSegment, TrackVia, PcbGraphicalLine, PcbGeneral, PcbSetup, Net


class PCB(AbstractParser):
    """PCB"""
    def __init__(self, child: AbstractParser|None = None) -> None:
        super().__init__(child)
        self.version: str = ""
        self.generator: str = ""
        self.uuid: str = ""
        self.paper: str = ""
        self.title_block: TitleBlock = TitleBlock()
        self.elements: List[BaseElement] = []

    def start(self, version: str, identifier: str, generator: str,
              paper: str, title_block: TitleBlock):
        self.version = version
        self.uuid = identifier
        self.generator = generator
        self.paper = paper
        self.title_block = title_block
        super().start(version, identifier, generator, paper, title_block)

    def visitPcbGeneral(self, general: PcbGeneral):
        """General Instance"""
        self.elements.append(general)
        super().visitPcbGeneral(general)

    def visitPcbSetup(self, setup: PcbSetup):
        """PCB setup Instance"""
        self.elements.append(setup)
        super().visitPcbSetup(setup)

    def startLayers(self):
        """Start Layers Instance"""
        super().startLayers()

    def endLayers(self):
        """End Layers Instance"""
        super().endLayers()

    def visitLayer(self, layer: PcbLayer):
        """Layer Instance"""
        self.elements.append(layer)
        super().visitLayer(layer)

    def visitSegment(self, segment: TrackSegment):
        """Track Segment Instance"""
        self.elements.append(segment)
        super().visitSegment(segment)

    def visitVia(self, via: TrackVia):
        """Track via instance"""
        self.elements.append(via)
        super().visitVia(via)

    def visitPcbGraphicalLine(self, graphical_line: PcbGraphicalLine):
        """PCB Graphical Line instance"""
        self.elements.append(graphical_line)
        super().visitPcbGraphicalLine(graphical_line)

    def visitNet(self, net: Net):
        """Net instance"""
        self.elements.append(net)
        super().visitNet(net)

    def produce(self, parser: AbstractParser):
        layers_started = False
        parser.start(self.version, self.uuid, self.generator, self.paper, None)
        for item in self.elements:
            if isinstance(item, PcbLayer):
                if not layers_started:
                    parser.startLayers()
                    layers_started = True
                parser.visitLayer(item)
            else:
                if layers_started:
                    parser.endLayers()
                    layers_started = False

                if isinstance(item, TrackVia):
                    parser.visitVia(item)
                elif isinstance(item, TrackSegment):
                    parser.visitSegment(item)
                elif isinstance(item, PcbGraphicalLine):
                    parser.visitPcbGraphicalLine(item)
                elif isinstance(item, PcbGeneral):
                    parser.visitPcbGeneral(item)
                elif isinstance(item, PcbSetup):
                    parser.visitPcbSetup(item)
                else:
                    print(f'Uknown Element: {item}')
        parser.end()
