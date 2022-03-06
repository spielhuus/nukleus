from typing import Dict, List, Set, Tuple

import numpy as np

from . import Circuit
from .model import POS_T, GlobalLabel, LocalLabel, Pin, Symbol, Wire
from .Schema import Schema


def bom(schema: Schema):

    # search for power and gnd and replace netnames
    result_bom = []
    for ref in schema.references():
        symbols = getattr(schema, ref)
        ref = symbols[0].property('Reference').value
        val = symbols[0].property('Value').value
        footprint = symbols[0].property('Footprint').value
        datasheet = ''
        for symbol in symbols:
            if symbol.has_property('Datasheet'):
                datasheet = symbol.property('Datasheet').value
        description = ''
        for symbol in symbols:
            if symbol.has_property('Description'):
                description = symbol.property('Description').value
        result_bom.append({'ref': ref, 'value': val, 'footprint': footprint,
                           'datasheet': datasheet, 'description': description})

    return {'bom': result_bom}
