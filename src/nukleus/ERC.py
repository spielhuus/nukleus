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

        symbols = nx.get_node_attributes(self.graph, 'symbol')
        for ref, symbols in self.references.items():
            #check if all units are on the schema
            # TODO
            for symbol in symbols:
                #check if symbol has Reference Number
                symbol_ref = symbol.property("Reference").value
                if symbol_ref.endswith("?"):
                    print(f'!!! no reference set in {symbol_ref}')

                #check if symbol a correct value
                if symbol.library_identifier == "Device:R":
                    print("check resistor")
                if symbol.library_identifier == "Device:C":
                    print("check capacitor")

                #check if all pins are connected
                #TODO

                #check connected types
                #TODO
