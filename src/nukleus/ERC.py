from typing import Dict, List, Set, Tuple

import numpy as np

from . import Circuit
from .model import POS_T, GlobalLabel, LocalLabel, Pin, Symbol, Wire
from .Schema import Schema
from .Spice import Net


def erc(schema: Schema, netlist: Dict[POS_T, Net]) -> List[List[str]]:



    # check if all pins are connected
    result_erc = []
    for sym in schema.elements:

    for ref in schema.references():
        symbol = getattr(schema, ref)
        result_bom.append([
            symbol[0].property('Reference').value,
            symbol[0].property('Value').value,
            symbol[0].property('Footprint').value,
            symbol[0].property('Datasheet').value,
            symbol[0].property('Description').value,
            ])

    return result_erc
