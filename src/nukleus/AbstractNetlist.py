from typing import Dict, List, Tuple

import networkx as nx

from .AbstractParser import AbstractParser
from .ModelSchema import (GlobalLabel, LocalLabel, NoConnect, Pin, PinImpl,
                          SchemaElement, Symbol, Wire)
from .transform import get_pins, transform
from .Typing import POS_T


class Net:
    """Netlist elemenet."""

    def __init__(self):
        self.identifier: str = str()
        """Netlist identifier."""
        self.netlist_type: str = 'normal'
        """Netlist type (normal, power) """
        self.coords = set()
        """Coordinates of the netlist."""
        self.pins: List[Pin] = []
        """Pins of the netlist."""

    def __str__(self) -> str:
        pins_string = []
        for pin in self.pins:
            ref_str = 'UNKNOWN'
            if isinstance(pin, PinImpl):
                ref_str = pin.parent.property('Reference').value
            pins_string.append(f'{ref_str} ({pin.number[0]})')
        return f"Net: {self.identifier}, coords: {self.coords}, pins: {pins_string}"


class AbstractNetlist(AbstractParser):
    """Calculate netlists for the schema."""

    def __init__(self, child: AbstractParser | None = None) -> None:
        super().__init__(child)
        self.graph = nx.MultiGraph()
        self.nodes: Dict[Tuple[float, float], SchemaElement] = {}
        self.references: Dict[str, List[Symbol]] = {}
        self.nets: Dict[POS_T, Net] = {}
        self.no_connect: Dict[POS_T, NoConnect] = {}

    def visitWire(self, wire: Wire):
        """Wire Symbol"""

        if wire.pts[0] in self.nodes:
            self.nodes[wire.pts[0]] = wire
        else:
            self.nodes[wire.pts[0]] = wire
        if wire.pts[1] in self.nodes:
            self.nodes[wire.pts[1]] = wire
        else:
            self.nodes[wire.pts[0]] = wire

        net0 = self.nets.get(wire.pts[0])
        net1 = self.nets.get(wire.pts[1])
        if net0 and net1:
            net = net0
            net.coords = net0.coords.union(net1.coords)
        elif net0:
            net = net0
        elif net1:
            net = net1
        else:
            net = Net()

        net.coords.add(wire.pts[0])
        net.coords.add(wire.pts[1])

        assert net, "net is not set"
        for coord in net.coords:
            self.nets[coord] = net

        super().visitWire(wire)

    def visitNoConnect(self, no_connect: NoConnect):
        """No Connect Symbol"""
        self.no_connect[no_connect.pos] = no_connect
        super().visitNoConnect(no_connect)

    def visitLocalLabel(self, local_label: LocalLabel):
        """Local Label"""
        self.nodes[local_label.pos] = local_label

        label_pos = local_label.pos
        net0 = self.nets.get(label_pos)
        if net0:
            net = net0
        else:
            net = Net()
            self.nets[label_pos] = net

        net.identifier = local_label.text
        assert net, "net is not set"
        net.coords.add(label_pos)

        super().visitLocalLabel(local_label)

    def visitGlobalLabel(self, global_label: GlobalLabel):
        """Global Label"""
        self.nodes[global_label.pos] = global_label

        label_pos = global_label.pos
        net0 = self.nets.get(label_pos)
        if net0:
            net = net0
        else:
            net = Net()
            self.nets[label_pos] = net

        net.identifier = global_label.text
        assert net, "net is not set"
        net.coords.add(label_pos)

        super().visitGlobalLabel(global_label)

    def visitSymbol(self, symbol: Symbol):
        """Symbol"""

        for pin in get_pins(symbol):
            pin_pos = transform(symbol, transform(pin))[0]
            self.nodes[pin_pos] = pin

        ref = symbol.property('Reference').value
        if ref in self.references:
            self.references[ref].append(symbol)
        else:
            self.references[ref] = [symbol]

        for pin in get_pins(symbol):
            pin_pos = transform(symbol, transform(pin))[0]
            net0 = self.nets.get(pin_pos)
            if net0:
                net = net0
            else:
                net = Net()
                self.nets[pin_pos] = net

            if symbol.library_identifier.startswith("power:"):
                net.identifier = symbol.property("Value").value
            assert net, "net is not set"
            net.coords.add(pin_pos)
            net.pins.append(pin)

        super().visitSymbol(symbol)

    def end(self):
        _id = 1
        for net in self.nets.values():
            if net.identifier == '':
                if len(net.coords) == 1 and next(iter(net.coords)) in self.no_connect:
                    net.identifier = "NC"
                else:
                    net.identifier = str(_id)
                _id += 1

        for ref in self.references.values():
            for symbol in ref:
                for pin in get_pins(symbol):
                    pin_pos = transform(symbol, transform(pin))[0]
                    self.graph.add_node(
                        self.nets[pin_pos].identifier, type='net')
                    self.graph.add_node(symbol.reference(),
                                        symbol=symbol, type='symbol')
                    self.graph.add_edge(
                        self.nets[pin_pos].identifier,
                        symbol.reference(),
                        key=f'{pin.parent.identifier}:{pin.number[0]}',
                        pin=pin,
                        net=self.nets[pin_pos].identifier)
        super().end()
