from typing import Dict, List, Set, Tuple

import numpy as np

from . import Circuit
from .model import POS_T, GlobalLabel, LocalLabel, Pin, Symbol, Wire
from .Schema import Schema



def bom(schema: Schema) -> List[List[str]]:

    # search for power and gnd and replace netnames
    result_bom = []
    for ref in schema.references():
        symbol = getattr(schema, ref)
        result_bom.append([
            symbol[0].property('Reference').value,
            symbol[0].property('Value').value,
            symbol[0].property('Footprint').value,
            symbol[0].property('Datasheet').value,
            symbol[0].property('Description').value,
            ])

    return result_bom
