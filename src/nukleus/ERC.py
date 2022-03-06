from typing import Dict, List, Set, Tuple

import numpy as np

from . import Circuit
from .model import POS_T, GlobalLabel, LocalLabel, Pin, Symbol, Wire
from .Schema import Schema
from .Spice import Net


def erc(schema: Schema, netlist: Dict[POS_T, Net]) -> List[List[str]]:



    # check if all pins are connected
    result_erc = []

    for ref in schema.references():
        symbol = getattr(schema, ref)

    return {'erc': result_erc}
