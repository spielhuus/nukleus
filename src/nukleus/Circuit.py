from __future__ import annotations
from typing import List, Dict

import networkx as nx
from nukleus.AbstractNetlist import AbstractNetlist

from nukleus.AbstractParser import AbstractParser
from nukleus.Registry import Registry
from .transform import get_pins
from .ModelSchema import Symbol

from .SpiceModel import get_includes, load_spice_models, spice_model


class Element:
    """Circuit element."""
    def __init__(self, ref: str, nodes: List[str], value: str):
        self.ref = ref
        """Reference of the element."""
        self.nodes = nodes
        """Nodes of the element."""
        self.value = value
        """Value of the element."""


class Resistor(Element):
    """Resistor element."""
    def __init__(self, ref: str, nodes: List[str], value: str):
        if not ref.startswith('R'):
            ref = f"R{ref}"
        super().__init__(ref, nodes, value)

    def __str__(self):
        return "{} {} {}".format(
            str(self.ref), " ".join(map(str, self.nodes)), self.value)


class Diode(Element):
    """Diode element."""
    def __init__(self, ref: str, nodes: List[str], value: str):
        if not ref.startswith('D'):
            ref = f"D{ref}"
        super().__init__(ref, nodes, value)

    def __str__(self):
        return "{} {} {}".format(
            str(self.ref), " ".join(map(str, self.nodes)), self.value)


class Capacitor(Element):
    """Capacitor element."""
    def __init__(self, ref: str, nodes: List[str], value: str):
        if not ref.startswith('C'):
            ref = f"C{ref}"
        super().__init__(ref, nodes, value)

    def __str__(self):
        return "{} {} {}".format(
            str(self.ref), " ".join(map(str, self.nodes)), self.value)


class Bjt(Element):
    """BJT element."""
#    def __init__(self, ref: str, nodes: List[str], value: str):
#        super().__init__(ref, nodes, value)

    def __str__(self):
        return "{} {} {}".format(
            str(self.ref), " ".join(map(str, self.nodes)), self.value)


class X(Element):
    """Subcircuit element."""
#    def __init__(self, ref: str, nodes: List[str], value: str):
#        super().__init__(ref, nodes, value)

    def __str__(self):
        return "X{} {} {}".format(
            str(self.ref), " ".join(map(str, self.nodes)), self.value)


class V(Element):
    """Voltage source element."""

    def __init__(self, ref: str, nodes: List[str], value: str):
        if not ref.startswith('V'):
            ref = f"V{ref}"
        super().__init__(ref, nodes, value)

    def __str__(self):
        return "V{} {} {}".format(
            str(self.ref), " ".join(map(str, self.nodes)), self.value)


class Circuit(AbstractNetlist):
    """
    Circuit class for creating netlist.
    """
    def __init__(self, child: AbstractParser | None = None) -> None:
        super().__init__(child)
        self.includes: List[spice_model] = []
        self.netlist: List[Element] = []
        self.subcircuits: Dict[str, Circuit] = {}
        self.spice_models: List[spice_model] = load_spice_models(Registry().spice_path)

    def subcircuit(self, circuit: SubCircuit) -> None:
        """
        Add a subcircuit.

        :param circuit: Circuit to add.
        :type circuit: Circuit
        :return: None
        :rtype: None
        """
        self.subcircuits[circuit.name] = circuit

    def R(self, ref: str, n0: str, n1: str, value: str) -> None:
        """
        Add a resistor

        :param ref: Resistor Reference
        :type ref: str
        :param n0: Node Name
        :type n0: str
        :param n1: Node Name
        :type n1: str
        :param value: Resistance value
        :type value: str
        :return: None
        :rtype: None
        """
        self.netlist.append(Resistor(ref, [n0, n1], value))

    def C(self, ref: str, n0: str, n1: str, value: str) -> None:
        """
        Add a capacitor

        :param ref: Node Reference
        :type ref: str
        :param n0: Node Name
        :type n0: str
        :param n1: Node Name
        :type n1: str
        :param value: Capacitance
        :type value: str
        :return: None
        :rtype: None
        """
        self.netlist.append(Capacitor(ref, [n0, n1], value))

    def D(self, ref: str, n0: str, n1: str, value: str) -> None:
        """
        Add a Diode

        :param ref: Node Reference
        :type ref: str
        :param n0: Node Name
        :type n0: str
        :param n1: Node Name
        :type n1: str
        :param value: Capacitance
        :type value: str
        :return: None
        :rtype: None
        """
        if value in self.subcircuits:
            pass
        else:
            get_includes(value, self.includes, self.spice_models)
        self.netlist.append(Diode(ref, [n0, n1], value))

    def Q(self, ref: str, n0: str, n1: str, n2: str, value: str) -> None:
        if value in self.subcircuits:
            pass
        else:
            get_includes(value, self.includes, self.spice_models)
        self.netlist.append(Bjt(ref, [n0, n1, n2], value))

    def X(self, ref: str, n: List[str], value: str):
        """
        Add subcircuit

        :param ref: Node Reference
        :type ref: str
        :param n: List of node names.
        :type n: List[str]
        :param value: None
        :type value: str
        """
        x = X(ref, n, value)
        if x.value not in self.subcircuits:
            get_includes(x.value, self.includes, self.spice_models)

        self.netlist.append(x)

    def V(self, ref: str, n1: str, n2: str, value: str):
        """
        Add voltage source

        :param ref: Node Reference
        :type ref: str
        :param n1: Node Name
        :type n1: str
        :param n2: Node Name
        :type n2: str
        :param value: Subcircuit name
        :type value: str
        """
        self.netlist.append(V(ref, [n1, n2], value))

    def __str__(self):
        res = ""
        for i in self.includes:
            res += f".include {i.path}\n"
        for i in self.subcircuits.values():
            res += f"{i}\n"
        for netlist in self.netlist:
            res += f"{netlist}\n"
        res += ".end\n"
        return res

    def __getattr__(self, name) -> Element:
        for netlist in self.netlist:
            if netlist.ref == name:
                return netlist

        raise AttributeError(f"No attribute {name}")

    """Calculate netlists for the schema."""
    @classmethod
    def _spice_primitive(cls, symbol, name) -> bool:
        return (
            symbol.has_property("Spice_Primitive")
            and symbol.property("Spice_Primitive").value == name
        ) or symbol.library_identifier == f"Device:{name}"

    @classmethod
    def _get_pinlist(cls, symbols: List[Symbol]) -> List[str]:
        #collect the pins of all symbols
        pins: List[str] = []
        for comp in symbols:
            assert comp.library_symbol, 'Library Symbol not set.'
            if comp.library_symbol.extends == "power":
                continue
            for pin in get_pins(comp):
                pins.append(pin.number[0])

        if all([item.isdigit() for item in pins]):
            pins.sort()
        return pins

    def end(self):
        super().end()
        symbols = nx.get_node_attributes(self.graph, 'symbol')
        #for symbol in symbols:
        for _, symbols in self.references.items():
            edge_list = []
            for _symbol in symbols:
                edge_list.extend(self.graph.edges(_symbol.reference(), keys=True, data=True))

            element: Symbol = symbols[0] #self.graph.nodes[symbol]['symbol']
            sym = element.library_symbol
            assert sym, 'Library Symbol not set.'
            if sym.extends == "power":
                pass

            elif (not element.has_property("Spice_Netlist_Enabled")
                  or element.property("Spice_Netlist_Enabled").value == "Y"):

                #get the pin order
                seq = Circuit._get_pinlist(symbols)
                if element.has_property("Spice_Node_Sequence"):
                    seq_field = element.property(
                        "Spice_Node_Sequence").value
                    seq = seq_field.split()

                #align the netnames with the pins
                nodes: List[str] = []
                for nlitem in seq:
                    for symbol in symbols:
                        for edges in edge_list:
                            if edges[2] == f'{symbol.identifier}:{nlitem}':
                                nodes.append(edges[3]['net'])

                if self._spice_primitive(element, "X"):
                    model = element.property("Spice_Model").value
                    self.X(element.property(
                        "Reference").value, nodes, model)

                elif self._spice_primitive(element, "R"):
                    res_value: str = element.property("Value").value
                    if res_value.lower().endswith("ohm"):
                        res_value = res_value[:-3]
                    # value = unit.parse_unit(value)
                    self.R(
                        element.property(
                            "Reference").value, nodes[0], nodes[1], res_value
                    )

                elif self._spice_primitive(element, "C"):
                    c_value = element.property("Value").value
                    # if value.lower().endswith('ohm'):
                    #    value = value[:-3]
                    # value = unit.parse_unit(value)
                    self.C(
                        element.property(
                            "Reference").value, nodes[0], nodes[1], c_value
                    )

#TODO
#                elif self._spice_primitive(element, "L"):
#                    if value.endswith("H"):
#                        value = value[:-1]
#                    # value = unit.parse_unit(value)
#                    self.L(element.reference, nets["1"], nets["2"], value)

                elif self._spice_primitive(element, "Q"):
                    model = element.property("Spice_Model").value
                    self.Q(
                        element.property(
                            "Reference").value, nodes[0], nodes[1], nodes[2], model
                    )

                elif self._spice_primitive(element, "D"):
                    model = element.property("Spice_Model").value
                    self.D(element.property("Reference").value, nodes[0], nodes[1], model)

                elif element.has_property("Spice_Primitive"):
                    print(
                        f'unknown spice primitive "{element.property("Spice_Primitive").value}"')

class SubCircuit(Circuit):
    """
    Subcircuit
    """
    def __init__(self, name: str, nodes: List[str]):
        super().__init__()
        self.name: str = name
        self.sub_nodes: List[str] = nodes

    def __str__(self):
        """Return the formatted subcircuit definition."""

        sub_nodes = " ".join(self.sub_nodes)
        strings: List[str] = []
        strings.append(f".subckt {self.name} {sub_nodes}")
        #strings.append(super().__str__())
        for netlist in self.netlist:
            strings.append(str(netlist))
        strings.append(f".ends {self.name}")
        return "\n".join(strings)
