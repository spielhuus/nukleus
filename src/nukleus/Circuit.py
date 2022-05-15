from __future__ import annotations
from typing import List, Dict

from nukleus.Registry import Registry

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


class Circuit():
    """
    Circuit class for creating netlist.
    """

    def __init__(self):
        self.includes: List[spice_model] = []
        self.netlist: List[Element] = []
        self.subcircuits: Dict[str, Circuit] = {}
        self.spice_models: List[spice_model] = load_spice_models(Registry().spice_path)

    def models(self, spice_models: List[spice_model]) -> None:
        """
        Add the spice models to this circuit.

        :param spice_models: List of spice models
        :type spice_models: List[spice_model]
        :return: None
        :rtype: None
        """
        self.spice_models = spice_models

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

class SubCircuit(Circuit):
    """
    Subcircuit
    """
    def __init__(self, name: str, nodes: List[str]):
        super().__init__()
        self.name: str = name
        self.nodes: List[str] = nodes

    def __str__(self):
        """Return the formatted subcircuit definition."""

        nodes = " ".join(self.nodes)
        strings: List[str] = []
        strings.append(f".subckt {self.name} {nodes}")
        #strings.append(super().__str__())
        for netlist in self.netlist:
            strings.append(str(netlist))
        strings.append(f".ends {self.name}")
        return "\n".join(strings)
