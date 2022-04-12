from typing import List, Dict, cast

from collections import deque
import re
import math
import numpy as np
from nptyping import NDArray, Shape, Float  # type: ignore

from .LibrarySymbol import LibrarySymbol
from .Pin import Pin, PinList
from .Symbol import Symbol
from .GraphicItem import Polyline, Rectangle, Circle
from .GlobalLabel import GlobalLabel
from .TextEffects import Justify
from .SchemaElement import POS_T, PTS_T
from .Footprint import Footprint

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

def totuple(a: NDArray[Shape["2, 2"], Float]):  # type: ignore
    if len(a) == 0:
        return a
    if isinstance(a[0], np.ndarray):
        return tuple(map(tuple, a))
    return (a[0], a[1])


def add(pos: POS_T, summand: POS_T) -> POS_T:
    """
    Add two positions.

    :param pos POS_T: Origin position.
    :param summand POS_T: The position to add.
    :rtype POS_T: Sum of the two positions.
    """
    return cast(POS_T, totuple(np.round(np.array(pos) + np.array(summand), 3)))

def sub(pos: POS_T, subtrahend: POS_T|PTS_T) -> POS_T:
    """
    Subtract two positions.

    :param pos POS_T: Origin position.
    :param subtrahend POS_T: The position to subtract.
    :rtype POS_T: Difference of the two positions.
    """
    return cast(POS_T, totuple(np.round(np.array(pos) - np.array(subtrahend), 3)))  # type: ignore

def mul(pos: POS_T, multiplier: POS_T) -> POS_T:
    """
    Multiply a position by a scalar.

    :param pos POS_T: Origin position.
    :param multiplier POS_T: The scalar to multiply by.
    :rtype POS_T: Multiplied position.
    """
    return cast(POS_T, totuple(np.round(np.array(pos) * np.array(multiplier), 3)))

def transform(symbol: Symbol|Pin|GlobalLabel, path=(0, 0)) -> PTS_T:
    """
    Transform the coordinates of a Symbol or Pin.

    :param symbol Symbol|Pin: Symbol or Pin
    :param path List[float]: points to transform relative to the Symbol.
    :rtype POS_T: Transformed coordinates
    :raises TypeError: When the element is not a Symbol or Pin.
    """
    if isinstance(symbol, Symbol):
        theta = np.deg2rad(-symbol.angle)
        trans = np.reshape(MIRROR[symbol.mirror], (2, 2)).T
        rot = np.array([[math.cos(theta), -math.sin(theta)],
                        [math.sin(theta), math.cos(theta)]])

        verts = np.matmul(path, rot)
        verts = np.matmul(verts, trans)
        verts = (symbol.pos + verts)
        verts = np.round(verts, 3)
        return cast(PTS_T, totuple(verts))

    if isinstance(symbol, Pin):
        theta = np.deg2rad(symbol.angle)
        rot = np.array([math.cos(theta), math.sin(theta)])
        verts = np.array([symbol.pos, symbol.pos + rot * symbol.length])
        verts = np.round(verts, 3)
        return cast(PTS_T, totuple(verts))

    if isinstance(symbol, Footprint):
        theta = np.deg2rad(symbol.angle)
        rot = np.array([[math.cos(theta), -math.sin(theta)],
                        [math.sin(theta), math.cos(theta)]])
        verts = np.matmul(path, rot)
        verts = (symbol.pos + verts)
        verts = np.round(verts, 3)
        return cast(PTS_T, totuple(verts))

    if isinstance(symbol, GlobalLabel):
        theta = np.deg2rad(symbol.angle)
        rot = np.array([[math.cos(theta), -math.sin(theta)],
                        [math.sin(theta), math.cos(theta)]])
        verts = np.matmul(path, rot)
        verts = (symbol.pos + verts)
        verts = np.round(verts, 3)
        return cast(PTS_T, totuple(verts))

    raise TypeError(f'unknown type {type(symbol)}')

def isUnit(symbol: LibrarySymbol, unit: int) -> bool:
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
    """
    Get the pins of a symbol.

    :param symbol Symbol: The symbol.
    :rtype PinList: The pins.
    """
    _pins = PinList()
    assert symbol.library_symbol, 'library symbol is not set'
    for subsym in symbol.library_symbol.units:
        if isUnit(subsym, symbol.unit):
            _pins.extend(symbol, subsym.pins)
    return _pins

def symbol_size(symbol: Symbol):
    """
    Calculate the Symbol size.

    :param symbol Symbol: [TODO:description]
    """
    sizes = []
    for unit in symbol.library_symbol.units:
        if isUnit(unit, symbol.unit):
            for graph in unit.graphics:
                if isinstance(graph, Polyline):
                    sizes.append(f_coord(np.array(graph.points)))
                elif isinstance(graph, Rectangle):
                    sizes.append(np.array([(graph.start_x, graph.start_y),
                                           (graph.end_x, graph.end_y)]))
                elif isinstance(graph, Circle):
                    sizes.append(np.array([(graph.center[0] - graph.radius,
                                            graph.center[1] + graph.radius),
                                           (graph.center[0] + graph.radius,
                                            graph.center[1] + graph.radius)]))
                else:
                    #raise TypeError(f'unknown type {type(graph)}')
                    print(f"TypeError(f'unknown type {type(graph)}')")
            for pin in unit.pins:
                sizes.append(transform(pin))

    if len(sizes) == 0:
        return np.array([[0, 0], [0, 0]])
    return f_coord(np.array(sizes))

def pinPosition(symbol) -> List[int]:
    positions = pinByPositions(symbol)
    return [len(positions['west']), len(positions['south']),
            len(positions['east']), len(positions['north'])]

def pinByPositions(symbol: Symbol) -> Dict[str, List[Pin]]:
    """
    Get a Dictionary with the Pins sorted by position.

    :param
    """
    position: deque[List[Pin]] = deque([[], [], [], []])

    for pin in get_pins(symbol):
        assert pin.angle <= 270, "pin angle greater then 270°"
        position[int(pin.angle / 90)].append(pin)

    if 'x' in symbol.mirror:
        pos1 = position[1]
        pos3 = position[3]
        position[1] = pos3
        position[3] = pos1

    if 'y' in symbol.mirror:
        pos0 = position[0]
        pos2 = position[2]
        position[2] = pos0
        position[0] = pos2

    position.rotate(int(symbol.angle/90))
    return {'west': position[0], 'south': position[1], 'east': position[2], 'north': position[3]}


def placeFields(symbol: Symbol) -> None:
    positions = pinPosition(symbol)
    # TODO print(f'placeFields: {symbol.angle} {symbol.property("Reference").value} {positions}')
    vis_fields = [x for x in symbol.properties if not x.text_effects.hidden]
    _size = f_coord(transform(symbol, symbol_size(symbol)))
    if len(get_pins(symbol)) == 1:
        if positions[0] == 1:
            vis_fields[0].pos = (_size[1][0]+1,28, symbol.pos[1])
            assert vis_fields[0].text_effects, "pin has no text_effects"
            vis_fields[0].text_effects.justify = [Justify.LEFT]

        elif positions[1] == 1:
            vis_fields[0].pos = (symbol.pos[0], _size[0][1]-1.28)
            assert vis_fields[0].text_effects, "pin has no text_effects"
            vis_fields[0].text_effects.justify = [Justify.CENTER]

        elif positions[2] == 1:
            vis_fields[0].pos = (_size[0][0]-1,28, symbol.pos[1])
            assert vis_fields[0].text_effects, "pin has no text_effects"
            vis_fields[0].text_effects.justify = [Justify.RIGHT]

        elif positions[3] == 1:
            vis_fields[0].pos = (symbol.pos[0], _size[1][1]+1.28)
            assert vis_fields[0].text_effects, "pin has no text_effects"
            vis_fields[0].text_effects.justify = [Justify.CENTER]
    else:
        if positions[1] == 0:
            #fields top
            top_pos = _size[0][1] - ((len(vis_fields)-1) * 2) - 1.28
            for pin in vis_fields:
                pin.pos = (symbol.pos[0], top_pos)
                assert pin.text_effects, "pin has no text_effects"
                pin.text_effects.justify = [Justify.CENTER]
                pin.angle = 90
                top_pos += 2

        elif positions[2] == 0:
            # fields west
            top_pos = _size[0][1] + \
                ((_size[1][1] - _size[0][1]) / 2) - \
                ((len(vis_fields)-1) * 2) / 2
            for pin in vis_fields:
                pin.pos = (_size[1][0]+0.762, top_pos)
                assert pin.text_effects, "pin has no text_effects"
                pin.text_effects.justify = [Justify.LEFT] if symbol.angle == 0 else [Justify.RIGHT]
                pin.angle = 0
                top_pos += 2

        elif positions[0] == 0:
            # fields east
            top_pos = _size[0][1] + \
                ((_size[1][1] - _size[0][1]) / 2) - \
                ((len(vis_fields)-1) * 2) / 2
            for pin in vis_fields:
                pin.pos = (_size[0][0]-0.762, top_pos)
                assert pin.text_effects, "pin has no text_effects"
                pin.text_effects.justify = [Justify.RIGHT] if symbol.angle == 0 else [Justify.LEFT]
                pin.angle = 0
                top_pos += 2
            #assert False, "implement"
        elif positions[3] == 0:
            assert False, "implement, single pin fields bottom"
        else:
            assert False, "implement, single pin all sides have pins"
