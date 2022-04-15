from __future__ import annotations

from typing import List, cast

from ..SexpParser import SEXP_T
from .SchemaElement import POS_T, PTS_T


class PcbZoneFillSettings:
    def __init__(
        self,
        filled: bool,
        mode: str,
        thermal_gap: str,
        thermal_bridge_width: str,
        smoothing: str,
        island_removal_mode: str,
        island_area_min: str,
        hatch_thickness: str,
        hatch_gap: str,
        hatch_orientation: str,
        hatch_smoothing_level: str,
        hatch_smoothing_value: str,
        hatch_border_algorithm: str,
        hatch_min_hole_area: str,
    ) -> None:

        self.filled: bool = filled
        self.mode: str = mode
        self.thermal_gap: str = thermal_gap
        self.thermal_bridge_width: str = thermal_bridge_width
        self.smoothing: str = smoothing
        self.island_removal_mode: str = island_removal_mode
        self.island_area_min: str = island_area_min
        self.hatch_thickness: str = hatch_thickness
        self.hatch_gap: str = hatch_gap
        self.hatch_orientation: str = hatch_orientation
        self.hatch_smoothing_level: str = hatch_smoothing_level
        self.hatch_smoothing_value: str = hatch_smoothing_value
        self.hatch_border_algorithm: str = hatch_border_algorithm
        self.hatch_min_hole_area: str = hatch_min_hole_area

    @classmethod
    def parse(cls, sexp: SEXP_T) -> PcbZoneFillSettings:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _filled: bool = False
        _mode: str = ''
        _thermal_gap: str = ''
        _thermal_bridge_width: str = ''
        _smoothing: str = ''
        _island_removal_mode: str = ''
        _island_area_min: str = ''
        _hatch_thickness: str = ''
        _hatch_gap: str = ''
        _hatch_orientation: str = ''
        _hatch_smoothing_level: str = ''
        _hatch_smoothing_value: str = ''
        _hatch_border_algorithm: str = ''
        _hatch_min_hole_area: str = ''

        for token in sexp[1:]:
            if token == 'yes':
                _filled = True
            elif token[0] == 'mode':
                _mode = token[1]
            elif token[0] == 'thermal_gap':
                _thermal_gap = token[1]
            elif token[0] == 'thermal_bridge_width':
                _thermal_bridge_width = token[1]
            elif token[0] == 'smoothing':
                _smoothing = token[1]
            elif token[0] == 'island_removal_mode':
                _island_removal_mode = token[1]
            elif token[0] == 'island_area_min':
                _island_area_min = token[1]
            elif token[0] == 'hatch_thickness':
                _hatch_thickness = token[1]
            elif token[0] == 'hatch_gap':
                _hatch_gap = token[1]
            elif token[0] == 'hatch_orientation':
                _hatch_orientation = token[1]
            elif token[0] == 'hatch_smoothing_level':
                _hatch_smoothing_level = token[1]
            elif token[0] == 'hatch_smoothing_value':
                _hatch_smoothing_value = token[1]
            elif token[0] == 'hatch_border_algorithm':
                _hatch_border_algorithm = token[1]
            elif token[0] == 'hatch_min_hole_area':
                _hatch_min_hole_area = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return PcbZoneFillSettings(_filled, _mode, _thermal_gap, _thermal_bridge_width, _smoothing,
                                   _island_removal_mode, _island_area_min, _hatch_thickness, _hatch_gap,
                                   _hatch_orientation, _hatch_smoothing_level, _hatch_smoothing_value,
                                   _hatch_border_algorithm, _hatch_min_hole_area)


class PcbFilledPolygon:
    def __init__(self, layer: str, pts: PTS_T) -> None:
        self.layer: str = layer
        self.pts: PTS_T = pts

    @classmethod
    def parse(cls, sexp: SEXP_T) -> PcbFilledPolygon:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _layer: str = str(sexp[1])
        _pts: PTS_T = []
        for pt in sexp[2][1:]:
            _pts.append((float(pt[1]), float(pt[2])))

        return PcbFilledPolygon(_layer, _pts)


class PcbZone:
    def __init__(
        self,
        net: str,
        net_name: str,
        layer: str,
        tstamp: str,
        name: str,
        hatch: str,
        priority: str,
        connect_pads: str,
        min_thickness: float,
        filled_areas_thickness: str,
        polygon: PTS_T,
        fill_settings: PcbZoneFillSettings,
        filled_polygon: PcbFilledPolygon
    ) -> None:

        self.net: str = net
        self.net_name: str = net_name
        self.layer: str = layer
        self.tstamp: str = tstamp
        self.name: str = name
        self.hatch: str = hatch
        self.priority: str = priority
        self.connect_pads: str = connect_pads
        self.min_thickness: float = min_thickness
        self.filled_areas_thickness: str = filled_areas_thickness
        self.polygon: PTS_T = polygon
        self.fill_settings: PcbZoneFillSettings = fill_settings
        self.filled_polygon: PcbFilledPolygon = filled_polygon

    @classmethod
    def parse(cls, sexp: SEXP_T) -> PcbZone:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _net: str = ''
        _net_name: str = ''
        _layer: str = ''
        _tstamp: str = ''
        _name: str = ''
        _hatch: str = ''
        _priority: str = ''
        _connect_pads: str = ''
        _min_thickness: float = 0.0
        _filled_areas_thickness: str = ''
        _polygon: PTS_T = []
        _fill_settings: PcbZoneFillSettings | None = None
        _filled_polygon: PcbFilledPolygon | None = None

        for token in sexp[1:]:
            if token[0] == 'net':
                _net = token[1]
            elif token[0] == 'net_name':
                _net_name = token[1]
            elif token[0] == 'layer':
                _layer = token[1]
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            elif token[0] == 'name':
                _name = token[1]
            elif token[0] == 'hatch':
                _hatch = token[1]
            elif token[0] == 'priority':
                _priority = token[1]
            elif token[0] == 'connect_pads':
                _connect_pads = token[1]
            elif token[0] == 'min_thickness':
                _min_thickness = float(token[1])
            elif token[0] == 'filled_areas_thickness':
                _filled_areas_thickness = token[1]
            elif token[0] == 'polygon':
                for pt in token[1][1:]:
                    _polygon.append((float(pt[1]), float(pt[2])))
            elif token[0] == 'fill':
                _fill_settings = PcbZoneFillSettings.parse(cast(SEXP_T, token))
            elif token[0] == 'filled_polygon':
                _filled_polygon = PcbFilledPolygon.parse(cast(SEXP_T, token))
            else:
                raise ValueError(f"Unexpected item: {token}")

        return PcbZone(_net, _net_name, _layer, _tstamp, _name, _hatch, _priority,
                       _connect_pads, _min_thickness, _filled_areas_thickness,
                       _polygon, _fill_settings, _filled_polygon)
