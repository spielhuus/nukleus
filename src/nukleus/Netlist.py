from nukleus.model.GlobalLabel import GlobalLabel
from nukleus.model.LibrarySymbol import LibrarySymbol
from nukleus.model.LocalLabel import LocalLabel
from nukleus.model.NoConnect import NoConnect
from nukleus.model.Symbol import Symbol
from nukleus.model.Utils import get_pins, transform
from nukleus.model.Wire import Wire

from .Circuit import Circuit
from .Schema import Schema


class Net():
    def __init__(self):
        self.id: str = str()
        self.coords = set()
        self.pins = []

    def __str__(self) -> str:
        return f'Net: {self.id}, coords: {self.coords}, pins: {self.pins}'


class Netlist():
    def __init__(self, schema: Schema) -> None:
        self.schema = schema
        self.nets = {}
        self.no_connect = []

        self._wires()
        self._labels()
        self._pins()
        self._no_connect()

        for _, value in self.nets.items():
            _id = 1
            if value.id == '':
                value.id = str(_id)
                _id += 1

    def _wires(self):
        """
        collect all the wires and create netlist.

        :param schema Schema: Schema Object.
        """
        for element in self.schema.elements:
            if isinstance(element, Wire):
                net0 = self.nets.get(element.pts[0])
                net1 = self.nets.get(element.pts[1])
                if net0 and net1:
                    net = net0
                    net.coords = net0.coords.union(net1.coords)
                elif net0:
                    net = net0
                elif net1:
                    net = net1
                else:
                    net = Net()
                    #id += 1

                net.coords.add(element.pts[0])
                net.coords.add(element.pts[1])

                assert net, "net is not set"
                for coord in net.coords:
                    self.nets[coord] = net

    def _pins(self):
        """
        Collect all the pins and store positions.

        :param schema Schema: Schema Object.
        """
        for element in self.schema.elements:
            if isinstance(element, Symbol):
                for pin in get_pins(element):
                    pin_pos = transform(element, transform(pin))[0]
                    net0 = self.nets.get(pin_pos)
                    if net0:
                        net = net0
                    else:
                        net = Net()
                        net.id = 'NC'
                        self.nets[pin_pos] = net

                    if element.library_identifier.startswith('power:'):
                        net.id = element.property('Value').value
                    assert net, "net is not set"
                    net.coords.add(pin_pos)
                    net.pins.append(pin)

    def _labels(self):
        """
        Collect all the labels and name the netlists.

        :param schema Schema: Schema Object.
        """
        for element in self.schema.elements:
            if isinstance(element, (LocalLabel, GlobalLabel)):
                label_pos = element.pos
                net0 = self.nets.get(label_pos)
                if net0:
                    net = net0
                else:
                    net = Net()
                    self.nets[label_pos] = net

                net.id = element.text
                assert net, "net is not set"
                net.coords.add(label_pos)

    def _no_connect(self):
        """
        Collect all the NoConnect coordinates.

        :param schema Schema: Schema Object.
        """
        for element in self.schema.elements:
            if isinstance(element, NoConnect):
                self.no_connect.append(element.pos)

    def erc(self):
        pass

    @classmethod
    def _spice_primitive(cls, symbol, name) -> bool:
        return (symbol.has_property('Spice_Primitive') and
                symbol.property('Spice_Primitive').value == name) or \
            symbol.library_identifier == f"Device:{name}"

    def spice(self, circuit: Circuit):
        power = {}
        for ref in self.schema.references():
            nets = {}
            for comp in getattr(self.schema, ref):
                sym = self.schema.getSymbol(
                    comp.library_identifier, LibrarySymbol)
                if sym.extends == 'power':
                    continue
                for pin in get_pins(comp):
                    verts = transform(comp, transform(pin)[0])
                    coord = (verts[0], verts[1])
                    net = self.nets.get(coord)

                    if not net:
                        assert False, "shoul nnot happen"
                        net = Net()  # id)
                        net.id = 'NC'
                        net.coords.add(coord)
                        # id += 1
                        nets[coord] = net

                    nets[pin.number[0]] = net.id

            element = getattr(self.schema, ref)[0]
            sym = self.schema.getSymbol(
                element.library_identifier, LibrarySymbol)  # TODO loaded twice
            if sym.extends == 'power':
                power[element.property('Value').value] = element
            elif not element.has_property("Spice_Netlist_Enabled") or \
                    element.property("Spice_Netlist_Enabled").value == "Y":

                if self._spice_primitive(element, 'X'):
                    # get the pin numbers/names
                    seq = [str(_) for _ in range(1, len(nets)+1)]
                    if element.has_property('Spice_Node_Sequence'):
                        seq_field = element.property(
                            'Spice_Node_Sequence').value
                        seq = seq_field.text.split()
                    elif not all(name in seq for name in nets.keys()):
                        # not all parts have numbered pins, get the pin names TODO
                        seq = nets.keys()

                    nodes = []
                    for arg in seq:
                        nodes.append(str(nets[str(arg)]))

                    model = element.property("Spice_Model").value
                    circuit.X(element.property(
                        "Reference").value, nodes, model)

                elif self._spice_primitive(element, 'R'):
                    value = element.property("Value").value
                    if value.lower().endswith('ohm'):
                        value = value[:-3]
                    # value = unit.parse_unit(value)
                    circuit.R(element.property("Reference").value,
                                nets['1'], nets['2'], value)

                elif self._spice_primitive(element, 'C'):
                    value = element.property("Value").value
                    # if value.lower().endswith('ohm'):
                    #    value = value[:-3]
                    # value = unit.parse_unit(value)
                    circuit.C(element.property("Reference").value,
                                nets['1'], nets['2'], value)

                elif self._spice_primitive(element, 'L'):
                    if value.endswith('H'):
                        value = value[:-1]
                    # value = unit.parse_unit(value)
                    circuit.L(element.reference,
                                nets['1'], nets['2'], value)
