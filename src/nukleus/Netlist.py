from typing import Dict, List, cast

from nukleus.AbstractParser import AbstractParser

from .ModelSchema import Pin, PinImpl, Symbol, NoConnect, LocalLabel, GlobalLabel, Wire
from .transform import get_pins, transform
from .Circuit import Circuit
from .Typing import POS_T, PTS_T

class Net:
    """Netlist elemenet."""

    def __init__(self):
        self.identifier: str = str()
        """Netlist identifier."""
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


class Netlist(AbstractParser):
    """Calculate netlists for the schema."""

    def __init__(self, child: AbstractParser|None = None) -> None:
        super().__init__(child)
        self.nets: Dict[POS_T, Net] = {}
        self.no_connect: List[POS_T] = []
        self.references: Dict[str, List[Symbol]] = {}

    def erc(self) -> List:
        return []

    @classmethod
    def _spice_primitive(cls, symbol, name) -> bool:
        return (
            symbol.has_property("Spice_Primitive")
            and symbol.property("Spice_Primitive").value == name
        ) or symbol.library_identifier == f"Device:{name}"

    def spice(self, circuit: Circuit):
        """
        Write the netlist to the circuit

        :param circuit Circuit: The circuit object.
        """
        _id = 1
        for _, value in self.nets.items():
            if value.identifier == "":
                if len(value.pins) > 1:
                    value.identifier = str(_id)
                    _id += 1
                else:
                    value.identifier = "NC"
        power = {}
        for ref in self.references.values():
            nets: Dict[str, str] = {}

            #collect the pins of all symbols
            for comp in ref:
                assert comp.library_symbol, 'Library Symbol not set.'
                if comp.library_symbol.extends == "power":
                    continue
                for pin in get_pins(comp):
                    verts: PTS_T = transform(comp, transform(pin)[0])
                    coord: POS_T = cast(POS_T, (verts[0], verts[1]))
                    net = self.nets.get(coord)

                    assert net, "net must be found."
                    nets[pin.number[0]] = net.identifier

            element: Symbol = ref[0]
            sym = element.library_symbol
            assert sym, 'Library Symbol not set.'
            if sym.extends == "power":
                power[element.property("Value").value] = element
            elif (not element.has_property("Spice_Netlist_Enabled")
                  or element.property("Spice_Netlist_Enabled").value == "Y"):

                if self._spice_primitive(element, "X"):
                    # get the pin numbers/names
                    seq = [str(_) for _ in range(1, len(nets) + 1)]
                    if element.has_property("Spice_Node_Sequence"):
                        seq_field = element.property(
                            "Spice_Node_Sequence").value
                        seq = seq_field.split()
                    elif not all(name in seq for name in nets):
                        # not all parts have numbered pins, get the pin names TODO
                        seq = list(nets.keys())

                    nodes = []
                    for arg in seq:
                        nodes.append(str(nets[str(arg)]))

                    model = element.property("Spice_Model").value
                    circuit.X(element.property(
                        "Reference").value, nodes, model)

                elif self._spice_primitive(element, "R"):
                    res_value: str = element.property("Value").value
                    if res_value.lower().endswith("ohm"):
                        res_value = res_value[:-3]
                    # value = unit.parse_unit(value)
                    circuit.R(
                        element.property(
                            "Reference").value, nets["1"], nets["2"], res_value
                    )

                elif self._spice_primitive(element, "C"):
                    c_value = element.property("Value").value
                    # if value.lower().endswith('ohm'):
                    #    value = value[:-3]
                    # value = unit.parse_unit(value)
                    circuit.C(
                        element.property(
                            "Reference").value, nets["1"], nets["2"], c_value
                    )
#TODO
#                elif self._spice_primitive(element, "L"):
#                    if value.endswith("H"):
#                        value = value[:-1]
#                    # value = unit.parse_unit(value)
#                    circuit.L(element.reference, nets["1"], nets["2"], value)

                elif self._spice_primitive(element, "Q"):
                    model = element.property("Spice_Model").value
                    circuit.Q(
                        element.property(
                            "Reference").value, nets["1"], nets["2"], nets["3"], model
                    )

                elif self._spice_primitive(element, "D"):
                    seq = [str(_) for _ in range(1, len(nets) + 1)]
                    if element.has_property("Spice_Node_Sequence"):
                        seq_field = element.property(
                            "Spice_Node_Sequence").value
                        seq = seq_field.split()
                    elif not all(name in seq for name in nets):
                        # not all parts have numbered pins, get the pin names
                        seq = list(nets.keys())

                    nodes = []
                    for arg in seq:
                        nodes.append(str(nets[str(arg)]))

                    model = element.property("Spice_Model").value
                    circuit.D(element.property("Reference").value, nodes[0], nodes[1], model)

                elif element.has_property("Spice_Primitive"):
                    print(
                        f'unknown spice primitive "{element.property("Spice_Primitive").value}"')

    def visitWire(self, wire: Wire):
        """Wire Symbol"""
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
        self.no_connect.append(no_connect.pos)
        super().visitNoConnect(no_connect)

    def visitLocalLabel(self, local_label: LocalLabel):
        """Local Label"""
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
                # TODO net.identifier = "NC"
                self.nets[pin_pos] = net

            if symbol.library_identifier.startswith("power:"):
                net.identifier = symbol.property("Value").value
            assert net, "net is not set"
            net.coords.add(pin_pos)
            net.pins.append(pin)
        super().visitSymbol(symbol)
