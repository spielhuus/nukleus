from __future__ import annotations

from typing import cast

from nukleus.model.FootprintAttributes import FootprintAttributes
from nukleus.model.FootprintGraphicsItems import (FootprintArc, FootprintGraphicsItems,
                                                  FootprintLine, FootprintText, FootprintCircle)
from nukleus.model.FootprintPad import FootprintPad
from nukleus.model.SchemaElement import POS_T

from ..SexpParser import SEXP_T


class Footprint():
    """
    The footprint token defines a footprint.
    """

    def __init__(self, library: str, locked: str, placed: str, layer: str, tedit: str,
                 tstamp: str, pos: str, angle: float, descr: str, tags: str, property: str, path: str,
                 autoplace_cost90: str, autoplace_cost180: str, solder_mask_margin: str,
                 solder_paste_margin: str, solder_paste_ratio: str, clearance: str,
                 zone_connect: str, thermal_width: str, thermal_gap: str, ATTRIBUTES: str,
                 GRAPHIC_ITEMS: str, pads: str, ZONES: str, GROUPS: str, MODEL: str) -> None:

        self.library = library
        self.locked = locked
        self.placed = placed
        self.layer = layer
        self.tedit = tedit
        self.tstamp = tstamp
        self.pos = pos
        self.angle = angle
        self.descr = descr
        self.tags = tags
        self.property = property
        self.path = path
        self.autoplace_cost90 = autoplace_cost90
        self.autoplace_cost180 = autoplace_cost180
        self.solder_mask_margin = solder_mask_margin
        self.solder_paste_margin = solder_paste_margin
        self.solder_paste_ratio = solder_paste_ratio
        self.clearance = clearance
        self.zone_connect = zone_connect
        self.thermal_width = thermal_width
        self.thermal_gap = thermal_gap
        self.ATTRIBUTES = ATTRIBUTES
        self.GRAPHIC_ITEMS = GRAPHIC_ITEMS
        self.pads = pads
        self.ZONES = ZONES
        self.GROUPS = GROUPS
        self.MODEL = MODEL

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Net:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype General: The Net Object.
        """
        _library: str = str(sexp[1])
        _locked: bool = False
        _placed: bool = False
        _layer: str = ''
        _tedit: str = ''
        _tstamp: str = ''
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _descr: str = ''
        _tags: str = ''
        _property: str = ''
        _path: str = ''
        _autoplace_cost90: str = ''
        _autoplace_cost180: str = ''
        _solder_mask_margin: str = ''
        _solder_paste_margin: str = ''
        _solder_paste_ratio: str = ''
        _clearance: str = ''
        _zone_connect: str = ''
        _thermal_width: str = ''
        _thermal_gap: str = ''
        _attributes: List = []
        _graphic_items: List = []
        _pads: List = []
        _zones: List = []
        _groups: List = []
        _model: List = []
        _pads: List[PcbPad] = []

        for token in sexp[2:]:
            if token[0] == 'locked':
                _locked = True
            elif token[0] == 'placed':
                _placed = True
            elif token[0] == 'layer':
                _layer = str(token[1])
            elif token[0] == 'tedit':
                _tedit = str(token[1])
            elif token[0] == 'tstamp':
                _tstamp = str(token[1])
            elif token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
                _pos = (float(token[1]), float(token[2]))
            elif token[0] == 'descr':
                _descr = str(token[1])
            elif token[0] == 'tags':
                _tags = str(token[1])
            elif token[0] == 'property':
                _property = str(token[1])
            elif token[0] == 'path':
                _path = str(token[1])
            elif token[0] == 'autoplace_cost90':
                _autoplace_cost90 = str(token[1])
            elif token[0] == 'autoplace_cost180':
                _autoplace_cost180 = str(token[1])
            elif token[0] == 'solder_mask_margin':
                _solder_paste_margin = str(token[1])
            elif token[0] == 'solder_paste_margin':
                _solder_paste_margin = str(token[1])
            elif token[0] == 'solder_paste_ratio':
                _solder_paste_ratio = str(token[1])
            elif token[0] == 'clearance':
                _clearance = str(token[1])
            elif token[0] == 'zone_connect':
                _zone_connect = str(token[1])
            elif token[0] == 'thermal_width':
                _thermal_width = str(token[1])
            elif token[0] == 'thermal_gap':
                _thermal_gap = str(token[1])
            elif token[0] == 'attr':
                _attributes.append(FootprintAttributes.parse(token))
            elif token[0] == 'fp_text':
                _graphic_items.append(FootprintText.parse(token))
            elif token[0] == 'fp_line':
                _graphic_items.append(FootprintLine.parse(token))
            elif token[0] == 'fp_circle':
                _graphic_items.append(FootprintCircle.parse(token))
            elif token[0] == 'fp_arc':
                _graphic_items.append(FootprintArc.parse(token))
            elif token[0] == 'pad':
                _pads.append(FootprintPad.parse(token))
#            elif token[0] == 'ZONES':
#            elif token[0] == 'GROUPS':
            elif token[0] == 'model':
                pass # TODO
            else:
                print('Unknown footprint token:', token)

        return Footprint(_library, _locked, _placed, _layer, _tedit, _tstamp, _pos,
                         _angle, _descr,
                         _tags, _property, _path, _autoplace_cost90, _autoplace_cost180,
                         _solder_mask_margin, _solder_paste_margin, _solder_paste_ratio,
                         _clearance, _zone_connect, _thermal_width, _thermal_gap, _attributes,
                         _graphic_items, _pads, _zones, _groups, _model)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        return f'{"  " * indent}(net {self.ordinal} {self.netname})'
