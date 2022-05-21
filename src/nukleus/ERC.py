from __future__ import annotations
from typing import List, Dict

import networkx as nx
from nukleus.AbstractNetlist import AbstractNetlist

from nukleus.AbstractParser import AbstractParser
from nukleus.Registry import Registry
from .transform import get_pins
from .ModelSchema import Symbol


class ERC(AbstractNetlist):
    """
    Circuit class for creating netlist.
    """
    def __init__(self, child: AbstractParser | None = None) -> None:
        super().__init__(child)

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






#        symbols = nx.get_node_attributes(self.graph, 'symbol')
#        #for symbol in symbols:
#        for _, symbols in self.references.items():
#            edge_list = []
#            for _symbol in symbols:
#                edge_list.extend(self.graph.edges(_symbol.reference(), keys=True, data=True))
#
#            element: Symbol = symbols[0] #self.graph.nodes[symbol]['symbol']
#            sym = element.library_symbol
#            assert sym, 'Library Symbol not set.'
#            if sym.extends == "power":
#                pass
#
#            elif (not element.has_property("Spice_Netlist_Enabled")
#                  or element.property("Spice_Netlist_Enabled").value == "Y"):
#
#                #get the pin order
#                seq = Circuit._get_pinlist(symbols)
#                if element.has_property("Spice_Node_Sequence"):
#                    seq_field = element.property(
#                        "Spice_Node_Sequence").value
#                    seq = seq_field.split()
#
#                #align the netnames with the pins
#                nodes: List[str] = []
#                for nlitem in seq:
#                    for symbol in symbols:
#                        for edges in edge_list:
#                            if edges[2] == f'{symbol.identifier}:{nlitem}':
#                                nodes.append(edges[3]['net'])
#
#                if self._spice_primitive(element, "X"):
#                    model = element.property("Spice_Model").value
#                    self.X(element.property(
#                        "Reference").value, nodes, model)
#
#                elif self._spice_primitive(element, "R"):
#                    res_value: str = element.property("Value").value
#                    if res_value.lower().endswith("ohm"):
#                        res_value = res_value[:-3]
#                    # value = unit.parse_unit(value)
#                    self.R(
#                        element.property(
#                            "Reference").value, nodes[0], nodes[1], res_value
#                    )
#
#                elif self._spice_primitive(element, "C"):
#                    c_value = element.property("Value").value
#                    # if value.lower().endswith('ohm'):
#                    #    value = value[:-3]
#                    # value = unit.parse_unit(value)
#                    self.C(
#                        element.property(
#                            "Reference").value, nodes[0], nodes[1], c_value
#                    )
#
##TODO
##                elif self._spice_primitive(element, "L"):
##                    if value.endswith("H"):
##                        value = value[:-1]
##                    # value = unit.parse_unit(value)
##                    self.L(element.reference, nets["1"], nets["2"], value)
#
#                elif self._spice_primitive(element, "Q"):
#                    model = element.property("Spice_Model").value
#                    self.Q(
#                        element.property(
#                            "Reference").value, nodes[0], nodes[1], nodes[2], model
#                    )
#
#                elif self._spice_primitive(element, "D"):
#                    model = element.property("Spice_Model").value
#                    self.D(element.property("Reference").value, nodes[0], nodes[1], model)
#
#                elif element.has_property("Spice_Primitive"):
#                    print(
#                        f'unknown spice primitive "{element.property("Spice_Primitive").value}"')
