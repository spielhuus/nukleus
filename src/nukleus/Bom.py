from typing import Dict, List, Set, Tuple

import numpy as np

from . import Circuit
from .model import POS_T, GlobalLabel, LocalLabel, Pin, Symbol, Wire
from .Schema import Schema


def _number(input):
    numbers = ''
    for char in input:
        if char.isdigit():
            numbers += char

    return int(numbers)


def _letter(input):
    letters = ''
    for char in input:
        if char.isalpha():
            letters += char

    return letters


def bom(schema: Schema, grouped: bool = True):

    # search for power and gnd and replace netnames
    result_bom = []
    target_sorted = {}
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

        target_sorted[('%s%03d' % (_letter(ref), _number(ref)))] = {
            'ref': ref,
            'value': val,
            'datasheet': datasheet,
            'description': description,
            'footprint': footprint
        }

    if grouped:
        target_grouped = {}
        for key in sorted(target_sorted):
            element = target_sorted[key]
            if ('%s-%s' % (element['value'], element['footprint'])) in target_grouped:
                target_grouped[('%s-%s' % (element['value'],
                                element['footprint']))]['ref'].append(element['ref'])
            else:
                target_grouped[('%s-%s' % (element['value'], element['footprint']))] = {
                    'ref': [element['ref']],
                    'value': element['value'],
                    'datasheet': element['datasheet'],
                    'description': element['description'],
                    'footprint': element['footprint']
                }

        result_bom = []
        for key in target_grouped:
            element = target_grouped[key]
            result_bom.append({
                'ref': element['ref'],
                'value': element['value'],
                'datasheet': element['datasheet'],
                'description': element['description'],
                'footprint': element['footprint']
            })

    return {'bom': result_bom}
