from typing import List

from collections import deque
import re
import math
import numpy as np
from nptyping import NDArray, Float

from .LibrarySymbol import LibrarySymbol
from .Pin import Pin, PinList
from .Symbol import Symbol
from .GraphicItem import Polyline, Rectangle
from .TextEffects import Justify
from .SchemaElement import POS_T, PTS_T

def f_coord(arr) -> PTS_T: 
    arr = np.array(arr)
    return [(np.min(arr[..., 0]), np.min(arr[..., 1])),
            (np.max(arr[..., 0]), np.max(arr[..., 1]))]
MIRROR = {
    '': np.array((1, 0, 0, -1)),
    'x': np.array((1, 0, 0, 1)),
    'y': np.array((-1, 0, 0, -1)),
    # 3: np.array((0, -1)),
}

def totuple(a: NDArray[Float]):
    if len(a) == 0:
        return a
    if isinstance(a[0], np.ndarray):
        return tuple(map(tuple, a))
    return (a[0], a[1])


def add(pos: POS_T, add: POS_T) -> POS_T:
    return totuple(np.array(pos) + np.array(add))

def sub(pos: POS_T, sub: POS_T) -> POS_T:
    return totuple(np.array(pos) - np.array(sub))

def transform(symbol: Symbol|Pin, path=(0, 0)) -> PTS_T:
    """
    Transform the coordinates of a Symbol or Pin.

    :param symbol Symbol|Pin: Symbol or Pin
    :param path List[float]: points to transform relative to the Symbol.
    :rtype POS_T: Transformed coordinates
    :raises TypeError: When the element is not a Symbol or Pin.
    """
    if isinstance(symbol, Symbol):
        theta = np.deg2rad(symbol.angle)
        trans = np.reshape(MIRROR[symbol.mirror], (2, 2)).T
        rot = np.array([[math.cos(theta), -math.sin(theta)],
                        [math.sin(theta), math.cos(theta)]])

        verts = np.matmul(path, rot)
        verts = np.matmul(verts, trans)
        verts = (symbol.pos + verts)
        verts = np.round(verts, 3)
        return totuple(verts)

    if isinstance(symbol, Pin):
        theta = np.deg2rad(symbol.angle)
        rot = np.array([math.cos(theta), math.sin(theta)])
        verts = np.array([symbol.pos, symbol.pos + rot * symbol.length])
        verts = np.round(verts, 3)
        return totuple(verts)

    raise TypeError(f'unknown type {type(symbol)}')

def is_unit(symbol: LibrarySymbol, unit: int) -> bool:
    """
    Test if LibrarySymbol is the given unit.

    :param symbol LibrarySymbol: The Library Sub-Symbol.
    :param unit int: The unit number.
    :rtype bool: True if the unit matches.
    """
    match = re.match(r".*_(\d+)_\d+", symbol.identifier)
    if match:
        _unit = int(match.group(1))
        return _unit in (0, (1 if unit == 0 else unit))
    return False

def get_pins(symbol: Symbol) -> PinList:
    _pins = PinList()
#        single_unit = False
    assert symbol.library_symbol, 'library symbol is not set'
    for subsym in symbol.library_symbol.units:
        if is_unit(subsym, symbol.unit):
#            unit = int(subsym.identifier.split('_')[-2])
#            single_unit = True if unit == 0 else single_unit
#            if unit == 0 or unit == self.unit or single_unit:
            _pins.extend(symbol, subsym.pins)
    return _pins

def symbol_size(symbol: Symbol):
    """
    Calculate the Symbol size.

    :param symbol Symbol: [TODO:description]
    """
    sizes = []
    for unit in symbol.library_symbol.units:
        if is_unit(unit, symbol.unit):
            for graph in unit.graphics:
                if isinstance(graph, Polyline):
                    sizes.append(f_coord(np.array(graph.points)))
                if isinstance(graph, Rectangle):
                    sizes.append(np.array([(graph.start_x, graph.start_y),
                                           (graph.end_x, graph.end_y)]))

            for pin in unit.pins:
                sizes.append(transform(pin))

    if len(sizes) == 0:
        return np.array([[0, 0], [0, 0]])
    return f_coord(np.array(sizes))

def pinPosition(symbol) -> List[int]: 
    res = deque([0, 0, 0, 0])

    for pin in get_pins(symbol):
        assert pin.angle <= 270, "pin angle greater then 270°"
        res[int(pin.angle / 90)] += 1

    if 'x' in symbol.mirror:
        pos0 = res[0]
        pos2 = res[2]
        res[0] = pos2
        res[2] = pos0

    if 'y' in symbol.mirror:
        pos1 = res[1]
        pos3 = res[3]
        res[1] = pos1
        res[3] = pos3

    res.rotate(int(symbol.angle/90))
    return list(res)

def placeFields(symbol: Symbol) -> None:
    positions = pinPosition(symbol)
    vis_fields = [x for x in symbol.properties if x.text_effects.hidden == False]
    _size = f_coord(transform(symbol, symbol_size(symbol)))
    if len(get_pins(symbol)) == 1:
        if positions[0] == 1:
            print("single pin, fields right")

        elif positions[1] == 1:
            vis_fields[0].pos = (symbol.pos[0], _size[0][1]-0.762)
            assert vis_fields[0].text_effects, "pin has no text_effects"
            vis_fields[0].text_effects.justify = [Justify.CENTER]

        elif positions[2] == 1:
            print("single pin, fields left")
            vis_fields[0].pos = (0, 2.54)
            assert vis_fields[0].text_effects, "pin has no text_effects"
            vis_fields[0].text_effects.justify = [Justify.CENTER]

        elif positions[3] == 1:
            vis_fields[0].pos = (symbol.pos[0], _size[1][1]+0.762)
            assert vis_fields[0].text_effects, "pin has no text_effects"
            vis_fields[0].text_effects.justify = [Justify.CENTER]
    else:
        if positions[1] == 0:
            top_pos = _size[0][1] - ((len(vis_fields)-1) * 2) - 0.762
            for pin in vis_fields:
                pin.pos = (symbol.pos[0], top_pos)
                assert pin.text_effects, "pin has no text_effects"
                pin.text_effects.justify = [Justify.CENTER]
                top_pos += 2

        elif positions[0] == 0:
            top_pos = _size[0][1] + \
                ((_size[1][1] - _size[0][1]) / 2) - \
                ((len(vis_fields)-1) * 2) / 2
            for pin in vis_fields:
                pin.pos = (_size[1][0]+0.762, top_pos)
                assert pin.text_effects, "pin has no text_effects"
                pin.text_effects.justify = [Justify.LEFT]
                top_pos += 2

        elif positions[2] == 0:
            print("fields bottom")
            assert False, "implement"
        elif positions[3] == 0:
            print("fields left")
            assert False, "implement"
        else:
            print("all sides have pins")
            assert False, "implement"
