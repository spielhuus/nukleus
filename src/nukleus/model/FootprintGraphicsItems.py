from __future__ import annotations

from typing import List, cast

from .SchemaElement import POS_T, PTS_T
from .StrokeDefinition import StrokeDefinition
from .TextEffects import TextEffects
from ..SexpParser import SEXP_T


class FootprintGraphicsItems():
    pass

class FootprintText(FootprintGraphicsItems):
    def __init__(self, text_type: str, text: str, pos: POS_T, angle: float,
            unlocked: str, layer: str, hide: bool, effects: TextEffects, tstamp: str) -> None:
        self.text_type: str = text_type
        self.text: str = text
        self.pos: POS_T = pos
        self.angle: float = angle
        self.unlocked: str = unlocked
        self.layer: str = layer
        self.hide: bool = hide
        self.effects: TextEffects = effects
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintText:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _text_type: str = str(sexp[1])
        _text: str = str(sexp[2])
        _pos: POS_T = (0, 0)
        _angle: float = 0.0
        _unlocked: str = ''
        _layer: str = ''
        _hide: bool = False
        _effects: TextEffects|None = None
        _tstamp: str = ''

        for token in sexp[3:]:
            if token[0] == "text_type":
                _text_type = token[1]
            elif token[0] == "text":
                _text = token[1]
            elif token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == "unlocked":
                _unlocked = token[1]
            elif token[0] == "layer":
                _layer = token[1]
            elif token[0] == "hide":
                _hide = True
            elif token[0] == "effects":
                _effects = TextEffects.parse(token)
            elif token[0] == "tstamp":
                _tstamp = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintText(_text_type, _text, _pos, _angle,
                _unlocked, _layer, _hide, _effects, _tstamp)

class FootprintTextBox(FootprintGraphicsItems):
    def __init__(self, locked: bool, type: str, text: str, start: POS_T, end: POS_T, pts: PTS_T,
            angle: float, layer: str, effects: TextEffects,
            stroke_definition: StrokeDefinition, tstamp: str) -> None:

        self.locked: bool = locked
        self.type: str = type
        self.text: str = text
        self.start: POS_T = start
        self.end: POS_T = end
        self.pts: PTS_T = pts
        self.angle: float = angle
        self.layer: str = layer
        self.effects: TextEffects = effects
        self.stroke_definition: StrokeDefinition = stroke_definition
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintTextBox:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """

        _type: str = str(sexp[1])
        _text: str = str(sexp[2])
        _locked: bool = False
        _start: POS_T = (0, 0)
        _end: POS_T = (0, 0)
        _pts: PTS_T = []
        _angle: float = 0.0
        _layer: str = ''
        _effects: TextEffects|None = None
        _stroke_definition: StrokeDefinition|None = None
        _tstamp: str = ''

        for token in sexp[3:]:
            if token[0] == 'locked':
                _locked = True
            elif token[0] == 'text':
                _text = token[1]
            elif token[0] == 'start':
                _start = (float(token[1]), float(token[2]))
            elif token[0] == 'end':
                _end = (float(token[1]), float(token[2]))
            elif token[0] == 'pts':
                for pts in token[1]:
                    _pts.append((float(pts[1]), float(pts[2])))
            elif token[0] == 'angle':
                _angle = float(token[1])
            elif token[0] == 'layer':
                _layer = str(token[1])
            elif token[0] == 'effects':
                _effects = TextEffects.parse(token)
            elif token[0] == 'stroke_definition':
                _stroke_definition = StrokeDefinition.parse(token)
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintTextBox(_locked, _text, _start, _end, _pts, _angle,
                _layer, _effects, _stroke_definition, _tstamp)

class FootprintLine(FootprintGraphicsItems):
    def __init__(self, start: POS_T, end: POS_T, layer: str, width: float,
            stroke_definition: StrokeDefinition, locked: bool, tstamp: str) -> None:

        self.start: POS_T = start
        self.end: POS_T = end
        self.layer: str = layer
        self.width: float = width
        self.stroke_definition: StrokeDefinition = stroke_definition
        self.locked: bool = locked
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintTextBox:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _start: POS_T = (0, 0)
        _end: POS_T = (0, 0)
        _layer: str = ''
        _width: float = 0.0
        _stroke_definition: StrokeDefinition|None = None
        _locked: bool = False
        _tstamp: str = ''

        for token in sexp[1:]:
            if token[0] == 'start':
                _start = (float(token[1]), float(token[2]))
            elif token[0] == 'end':
                _end = (float(token[1]), float(token[2]))
            elif token[0] == 'layer':
                _layer = str(token[1])
            elif token[0] == 'width':
                _width = float(token[1])
            elif token[0] == 'stroke_definition':
                _stroke_definition = StrokeDefinition.parse(token)
            elif token[0] == 'locked':
                _locked = True
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintLine(_start, _end, _layer, _width, _stroke_definition,
                _locked, _tstamp)

class FootprintRectangle(FootprintGraphicsItems):
    def __init__(self, start: POS_T, end: POS_T, layer: str, width: float,
            stroke_definition: StrokeDefinition, fill: str, locked: bool, tstamp: str) -> None:
        self.start : POS_T = start
        self.end: POS_T = end
        self.layer : str = layer
        self.width: float = width
        self.stroke_definition: StrokeDefinition = stroke_definition
        self.fill: str = fill
        self.locked: bool = locked
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintRectangle:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _start: POS_T = (0, 0)
        _end: POS_T = (0, 0)
        _layer : str = ''
        _width: float = 0.0
        _stroke_definition: StrokeDefinition|None = None
        _fill: str = ''
        _locked: bool = False
        _tstamp: str = ''

        for token in sexp[1:]:
            if token[0] == 'start':
                _start = (float(token[1]), float(token[2]))
            elif token[0] == 'end':
                _end = (float(token[1]), float(token[2]))
            elif token[0] == 'layer':
                _layer = str(token[1])
            elif token[0] == 'width':
                _width = float(token[1])
            elif token[0] == 'stroke_definition':
                _stroke_definition = StrokeDefinition.parse(token)
            elif token[0] == 'fill':
                _fill = token[1]
            elif token[0] == 'locked':
                _locked = True
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintRectangle(_start, _end, _layer, _width, _stroke_definition,
                _fill, _locked, _tstamp)


class FootprintCircle(FootprintGraphicsItems):
    def __init__(self, center: POS_T, end: POS_T, layer: str, width: float,
            stroke_definition: StrokeDefinition, fill: str, locked: bool, tstamp: str) -> None:

        self.center: POS_T = center
        self.end: POS_T = end
        self.layer: str = layer
        self.width: float = width
        self.stroke_definition: StrokeDefinition = stroke_definition
        self.fill: str = fill
        self.locked: bool = locked
        self.tstamp: str = ''

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintCircle:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _center: POS_T = (0, 0)
        _end: POS_T = (0, 0)
        _layer: str = ''
        _width: float = 0.0
        _stroke_definition: StrokeDefinition|None = None
        _fill: str = ''
        _locked: bool = False
        _tstamp: str = ''

        for token in sexp[1:]:
            if token[0] == 'center':
                _center = (float(token[1]), float(token[2]))
            elif token[0] == 'end':
                _end = (float(token[1]), float(token[2]))
            elif token[0] == 'layer':
                _layer = str(token[1])
            elif token[0] == 'width':
                _width = float(token[1])
            elif token[0] == 'stroke_definition':
                _stroke_definition = StrokeDefinition.parse(token)
            elif token[0] == 'fill':
                _fill = token[1]
            elif token[0] == 'locked':
                _locked = True
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintCircle(_center, _end, _layer, _width, _stroke_definition,
                _fill, _locked, _tstamp)


class FootprintArc(FootprintGraphicsItems):
    def __init__(self, start: POS_T, mid: POS_T, end: POS_T, layer: str, width: float,
            stroke_definition: StrokeDefinition, fill: str, locked: bool, tstamp: str) -> None:
        self.start : POS_T = start
        self.mid: POS_T = end
        self.end: POS_T = end
        self.layer : str = layer
        self.width: float = width
        self.stroke_definition: StrokeDefinition = stroke_definition
        self.fill: str = fill
        self.locked: bool = locked
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintArc:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _start: POS_T = (0, 0)
        _mid: POS_T = (0, 0)
        _end: POS_T = (0, 0)
        _layer : str = ''
        _width: float = 0.0
        _stroke_definition: StrokeDefinition|None = None
        _fill: str = ''
        _locked: bool = False
        _tstamp: str = ''

        for token in sexp[1:]:
            if token[0] == 'start':
                _start = (float(token[1]), float(token[2]))
            elif token[0] == 'mid':
                _mid = (float(token[1]), float(token[2]))
            elif token[0] == 'end':
                _end = (float(token[1]), float(token[2]))
            elif token[0] == 'layer':
                _layer = str(token[1])
            elif token[0] == 'width':
                _width = float(token[1])
            elif token[0] == 'stroke_definition':
                _stroke_definition = StrokeDefinition.parse(token)
            elif token[0] == 'fill':
                _fill = token[1]
            elif token[0] == 'locked':
                _locked = True
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintArc(_start, _mid, _end, _layer, _width, _stroke_definition,
                _fill, _locked, _tstamp)


class FootprintPolygon(FootprintGraphicsItems):
    def __init__(self, pts: PTS_T, layer: str, width: float,
            stroke_definition: StrokeDefinition, fill: str, locked: bool, tstamp: str) -> None:
        self.pts : PTS_T = pts
        self.layer : str = layer
        self.width: float = width
        self.stroke_definition: StrokeDefinition = stroke_definition
        self.fill: str = fill
        self.locked: bool = locked
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintPolygon:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _pts: PTS_T = []
        _layer : str = ''
        _width: float = 0.0
        _stroke_definition: StrokeDefinition|None = None
        _fill: str = ''
        _locked: bool = False
        _tstamp: str = ''

        for token in sexp[1:]:
            if token[0] == 'COORDINATE_POINT_LIST':
                for pt in token[1:]:
                    _pts.append((float(pt[0]), float(pt[1])))
            elif token[0] == 'layer':
                _layer = str(token[1])
            elif token[0] == 'width':
                _width = float(token[1])
            elif token[0] == 'stroke_definition':
                _stroke_definition = StrokeDefinition.parse(token)
            elif token[0] == 'fill':
                _fill = token[1]
            elif token[0] == 'locked':
                _locked = True
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintPolygon(_pts, _layer, _width, _stroke_definition,
                _fill, _locked, _tstamp)

class FootprintCurve(FootprintGraphicsItems):
    def __init__(self, pts: PTS_T, layer: str, width: float,
            stroke_definition: StrokeDefinition, locked: bool, tstamp: str) -> None:
        self.pts : PTS_T = pts
        self.layer : str = layer
        self.width: float = width
        self.stroke_definition: StrokeDefinition = stroke_definition
        self.locked: bool = locked
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintCurve:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _pts: PTS_T = []
        _layer : str = ''
        _width: float = 0.0
        _stroke_definition: StrokeDefinition|None = None
        _locked: bool = False
        _tstamp: str = ''

        for token in sexp[1:]:
            if token[0] == 'COORDINATE_POINT_LIST':
                for pt in token[1:]:
                    _pts.append((float(pt[0]), float(pt[1])))
            elif token[0] == 'layer':
                _layer = str(token[1])
            elif token[0] == 'width':
                _width = float(token[1])
            elif token[0] == 'stroke_definition':
                _stroke_definition = StrokeDefinition.parse(token)
            elif token[0] == 'locked':
                _locked = True
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintCurve(_pts, _layer, _width, _stroke_definition,
                _locked, _tstamp)

