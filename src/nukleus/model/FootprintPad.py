from __future__ import annotations

from typing import List, cast

from nukleus.model.PcbGraphicItems import PcbGraphicsItems, PcbPolygon

from ..SexpParser import SEXP_T
from .SchemaElement import POS_T


class FootprintPadOptions:
    def __init__(self, clearance: str, anchor: str) -> None:
        self.clearance: str = clearance
        self.anchor: str = anchor

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintPadOptions:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _clearance: str = ''
        _anchor: str = ''

        for token in sexp[4:]:
            if token[0] == 'clearance':
                _clearance = token[1]
            elif token[0] == 'anchor':
                _anchor = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintPadOptions(_clearance, _anchor)


class FootprintPadPrimitives:
    def __init__(self,
        pcb_graphics: List[PcbGraphicsItems],
        width: float,
        fill: bool) -> None:

        self.pcb_graphics: List[PcbGraphicsItems] = pcb_graphics
        self.width: float = width
        self.fill: bool = fill

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintPadPrimitives:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _pcb_graphics: List[PcbGraphicsItems] = []
        _width: float = 0.0
        _fill: bool = False

        for token in sexp[1:]:
            if token[0] == 'width':
                _width = float(token[1])
            elif token[0] == 'fill':
                _fill = token[1]
            elif token[0] == 'gr_poly':
                _pcb_graphics.append(PcbPolygon.parse(token))
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintPadPrimitives(_pcb_graphics, _width, _fill)


class FootprintPad:
    def __init__(
        self,
        number: str,
        pad_type: str,
        shape: str,
        pos: POS_T,
        angle: float,
        locked: bool,
        size: float,
        drill: str,
        layers: str,
        property: str,
        remove_unused_layer: str,
        keep_end_layers: str,
        roundrect_rratio: str,
        chamfer_ratio: str,
        chamfer: str,
        net: str,
        tstamp: str,
        pinfunction: str,
        pintype: str,
        die_length: str,
        solder_mask_margin: str,
        solder_paste_margin: str,
        solder_paste_margin_ratio: str,
        clearance: str,
        zone_connect: str,
        thermal_width: str,
        thermal_gap: str,
        options: FootprintPadOptions,
        primitives: FootprintPadPrimitives
    ) -> None:

        self.number: str = number
        self.pad_type: str = pad_type
        self.shape: str = shape
        self.pos: POS_T = pos
        self.angle: float = angle
        self.locked: bool = locked
        self.size: float = size
        self.drill: str = drill
        self.layers: str = layers
        self.property: str = property
        self.remove_unused_layer: str = remove_unused_layer
        self.keep_end_layers: str = keep_end_layers
        self.roundrect_rratio: str = roundrect_rratio
        self.chamfer_ratio: str = chamfer_ratio
        self.chamfer: str = chamfer
        self.net: str = net
        self.tstamp: str = tstamp
        self.pinfunction: str = pinfunction
        self.pintype: str = pintype
        self.die_length: str = die_length
        self.solder_mask_margin: str = solder_mask_margin
        self.solder_paste_margin: str = solder_paste_margin
        self.solder_paste_margin_ratio: str = solder_paste_margin_ratio
        self.clearance: str = clearance
        self.zone_connect: str = zone_connect
        self.thermal_width: str = thermal_width
        self.thermal_gap: str = thermal_gap
        self.options: FootprintPadOptions = options
        self.primitives: FootprintPadPrimitives = primitives

    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintPad:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _number: str = str(sexp[1])
        _pad_type: str = str(sexp[2])
        _shape: str = str(sexp[3])
        _pos: POS_T = (0, 0)
        _angle: float = 0.0
        _locked: bool = False
        _size: float = 0.0
        _drill: str = ''
        _layers: str = ''
        _property: str = ''
        _remove_unused_layer: str = ''
        _keep_end_layers: str = ''
        _roundrect_rratio: str = ''
        _chamfer_ratio: str = ''
        _chamfer: str = ''
        _net: str = ''
        _tstamp: str = ''
        _pinfunction: str = ''
        _pintype: str = ''
        _die_length: str = ''
        _solder_mask_margin: str = ''
        _solder_paste_margin: str = ''
        _solder_paste_margin_ratio: str = ''
        _clearance: str = ''
        _zone_connect: str = ''
        _thermal_width: str = ''
        _thermal_gap: str = ''
        _options: FootprintPadOptions|None = None
        _primitives: FootprintPadPrimitives|None = None

        for token in sexp[4:]:
            if token[0] == 'number':
                _number = token[1]
            elif token[0] == 'pad_type':
                _pad_type = token[1]
            elif token[0] == 'shape':
                _shape = token[1]
            elif token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token == 'locked':
                _locked = True
            elif token[0] == 'size':
                _size = float(token[1])
            elif token[0] == 'drill':
                _drill = token[1]
            elif token[0] == 'layers':
                _layers = token[1]
            elif token[0] == 'property':
                _property = token[1]
            elif token[0] == 'remove_unused_layer':
                _remove_unused_layer = token[1]
            elif token[0] == 'keep_end_layers':
                _keep_end_layers = token[1]
            elif token[0] == 'roundrect_rratio':
                _roundrect_rratio = token[1]
            elif token[0] == 'chamfer_ratio':
                _chamfer_ratio = token[1]
            elif token[0] == 'chamfer':
                _chamfer = token[1]
            elif token[0] == 'net':
                _net = token[1]
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            elif token[0] == 'pinfunction':
                _pinfunction = token[1]
            elif token[0] == 'pintype':
                _pintype = token[1]
            elif token[0] == 'die_length':
                _die_length = token[1]
            elif token[0] == 'solder_mask_margin':
                _solder_mask_margin = token[1]
            elif token[0] == 'solder_paste_margin':
                _solder_paste_margin = token[1]
            elif token[0] == 'solder_paste_margin_ratio':
                _solder_paste_margin_ratio = token[1]
            elif token[0] == 'clearance':
                _clearance = token[1]
            elif token[0] == 'zone_connect':
                _zone_connect = token[1]
            elif token[0] == 'thermal_width':
                _thermal_width = token[1]
            elif token[0] == 'thermal_gap':
                _thermal_gap = token[1]
            elif token[0] == 'options':
                _thermal_gap = FootprintPadOptions.parse(token)
            elif token[0] == 'primitives':
                _thermal_gap = FootprintPadPrimitives.parse(token)
            else:
                raise ValueError(f"Unexpected item: {token}")

        return FootprintPad(_number, _pad_type, _shape, _pos, _angle, _locked, _size,
                _drill, _layers, _property, _remove_unused_layer, _keep_end_layers,
                _roundrect_rratio, _chamfer_ratio, _chamfer, _net, _tstamp,
                _pinfunction, _pintype, _die_length, _solder_mask_margin,
                _solder_paste_margin, _solder_paste_margin_ratio, _clearance,
                _zone_connect, _thermal_width, _thermal_gap, _options, _primitives)
