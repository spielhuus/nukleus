from typing import List, Dict, Set, Tuple

import glob
import math
import numpy as np
import os
import re

from . import Circuit
from .Schema import Schema

from .model import GlobalLabel, LocalLabel, Symbol, Pin, Wire, POS_T


class Net(object):
    def __init__(self, id: str):
        self.id: str = id
        self.coords: Set[POS_T] = set()
        self.pins: List[Pin] = []

    def __str__(self) -> str:
        return f"Net({self.id}, {self.coords} {self.id})"


def netlist(schema: Schema) -> Dict[POS_T, Net]:
    d: Dict[POS_T, Net] = {}
    id: int = 1

    # get the named netlists
    for text in schema.get_elements(LocalLabel):
        c = text.pos
        net: Net | None = d.get(c)
        net = Net(text.text)
        net.coords.add(c)
        d[c] = net

    for text in schema.get_elements(GlobalLabel):
        c = text.pos
        net: Net | None = d.get(c)
        net = Net(text.text)
        net.coords.add(c)
        d[c] = net

    # search for power and gnd and replace netnames
    for comp in schema.get_elements(Symbol):
        lib = schema.getSymbol(comp.library_identifier)
        if lib.extends == 'power':
            for subsym in lib.units:
                for pin in subsym.pins:
                    vert = comp._pos(pin._pos())
                    c = (vert[0][0], vert[0][1])
                    net = d.get(c)
                    if not net:
                        net = Net(comp.property('Value').value)
                        net.coords.add(c)
                        d[c] = net

                    net.pins.append(
                        (comp.property('Reference').value, pin.name, pin))
                    d[c] = net

    for wire in schema.get_elements(Wire):
        print(wire)
        c0 = (wire.pts[0])
        c1 = (wire.pts[1])
        net0 = d.get(c0)
        net1 = d.get(c1)

        if net0 and net1:
            net = net0
            net.coords = net0.coords.union(net1.coords)

        elif net0:
            net = net0
        elif net1:
            net = net1
        else:
            net = Net(str(id))
            id += 1

        net.coords.add(c0)
        net.coords.add(c1)

        for c in net.coords:
            d[c] = net

    return d


def _spice_primitive(symbol, name) -> bool:
    return (symbol.has_property('Spice_Primitive') and
            symbol.property('Spice_Primitive').value == name) or \
            symbol.library_identifier == f"Device:{name}"


def schema_to_spice(schema: Schema, circuit: Circuit,
                    d: Dict[Tuple[int, int], Net]) -> None:

    # loop symbols and get the pins
    refs = schema.references()
    for ref in refs:
        nets = {}
        for comp in getattr(schema, ref):
            sym = schema.getSymbol(comp.library_identifier)
            if sym.extends == 'power':
                continue
            single_unit = False
            for subsym in sym.units:
                unit = int(subsym.identifier.split('_')[-2])
                single_unit = True if unit == 0 else single_unit
                if unit == 0 or unit == comp.unit or single_unit:
                    for pin in subsym.pins:
                        verts = comp._pos(pin._pos()[0])  # TODO[0]
                        c = (verts[0], verts[1])
                        net = d.get(c)

                        if not net:
                            net = Net("NC")  # id)
                            net.coords.add(c)
                            # id += 1
                            d[c] = net

                        nets[pin.number[0]] = net.id

        for comp in getattr(schema, ref):
            if not comp.has_property("Spice_Netlist_Enabled") or \
            comp.property("Spice_Netlist_Enabled").value == "Y":
                if comp.has_property("Spice_Primitive") and \
                comp.property("Spice_Primitive").value == 'X':

                    # get the pin numbers/names
                    seq = [str(_) for _ in range(1, len(nets)+1)]
                    print(f"+{seq}")
                    print(f"-{nets.keys()}")
                    if comp.has_property('Spice_Node_Sequence'):
                        print(f'has_spice_node_seqence {comp.property("Spice_Node_Sequence").value}')
                        seq_field = comp.property('Spice_Node_Sequence').value
                        seq = seq_field.text.split()
                    elif not all(name in seq for name in nets.keys()):
                        # not all parts have numbered pins, get the pin names TODO
                        print(f"get names: {nets.keys()}")
                        seq = nets.keys()

                    print(f"seq {seq}")

                    nodes = []
                    for arg in seq:
                        nodes.append(str(nets[str(arg)]))

                    model = comp.property("Spice_Model").value
                    circuit.X(comp.property("Reference").value, nodes, model)

                elif _spice_primitive(comp, 'R'):
                    value = comp.property("Value").value
                    if value.lower().endswith('ohm'):
                        value = value[:-3]
                    # value = unit.parse_unit(value)
                    print(comp.property("Reference").value)
                    circuit.R(comp.property("Reference").value,
                            nets['1'], nets['2'], value)

                elif _spice_primitive(comp, 'C'):
                    value = comp.property("Value").value
                    # if value.lower().endswith('ohm'):
                    #    value = value[:-3]
                    # value = unit.parse_unit(value)
                    circuit.C(comp.property("Reference").value,
                            nets['1'], nets['2'], value)

                elif _spice_primitive(comp, 'L'):
                    if value.endswith('H'):
                        value = value[:-1]
                    # value = unit.parse_unit(value)
                    circuit.L(comp.reference, nets['1'], nets['2'], value)


class spice_model:
    def __init__(self, keys, path, includes, content):
        self.keys = keys
        self.path = path
        self.includes = includes
        self.content = content


def __load_model__(filename: str):
    with open(filename) as file:
        content = file.read()
        keys = []
        includes = []
        for m in re.findall(r"\.SUBCKT ([a-zA-Z0-9]*) .*", content, re.IGNORECASE):
            keys.append(m)
        for m in re.findall(r"\.include (.*)", content, re.IGNORECASE):
            includes.append(m)

        return(spice_model(keys, filename, includes, content))


def load_spice_models(paths: List[str]) -> List[spice_model]:
    for path in paths:
        models = []
        for filename in glob.iglob(f'{path}/**', recursive=True):
            if filename in (".", ".."):
                continue
            if os.path.splitext(filename)[-1].lower() in (".lib", ".mod"):
                models.append(__load_model__(filename))

    return models


def __model_by_path__(path, models):
    for m in models:
        filename = m.path.split("/")[-1]
        if path == filename:
            return m

    print(f"Model not found: {path}")
    return None


def __contains__(path, includes):
    for i in includes:
        if i.path == path:
            return True
    return False


def __get_includes__(path, includes, models):
    if not __contains__(path, includes):
        model = __model_by_path__(path, models)
        includes.append(model)
        for i in model.includes:
            __get_includes__(i)


def get_includes(key, includes, models):
    found = False
    for m in models:
        if key in m.keys:
            found = True
            if not __contains__(m.path, includes):
                includes.append(m)
                for i in m.includes:
                    __get_includes__(i, includes, models)

    assert found, f"Model not found {key}"
