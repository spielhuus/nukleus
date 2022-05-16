import math
from copy import deepcopy
from os import wait
from typing import IO, Any, Dict, cast

import numpy as np

from nukleus.plot.PlotSvgWrite import PlotSvgWrite
from nukleus.Registry import Registry

from .AbstractParser import AbstractParser
from .ModelBase import Justify, StrokeDefinition, TextEffects, TitleBlock, rgb
from .ModelSchema import (Arc, Circle, GlobalLabel, Junction, LibrarySymbol,
                          LocalLabel, NoConnect, Pin, Polyline, Property,
                          Rectangle, Symbol, Wire, isUnit)
from .Theme import themes
from .transform import transform
from .Typing import POS_T, PTS_T

MIRROR = {
    '': np.array((1, 0, 0, -1)),
    'x': np.array((1, 0, 0, 1)),
    'y': np.array((-1, 0, 0, -1)),
    # 3: np.array((0, -1)),
}


def _merge_text_effects(effects: TextEffects | None, theme: TextEffects) -> TextEffects:
    if not effects:
        return TextEffects(face=theme.face, font_width=theme.font_width,
                           font_height=theme.font_height, font_thickness=theme.font_thickness,
                           font_style=theme.font_style, justify=theme.justify,
                           hidden=theme.hidden)

    result: Dict[str, Any] = {}
    if effects.face == '':
        result['face'] = theme.face
    else:
        result['face'] = effects.face
    if effects.font_width == 0:
        result['font_width'] = theme.font_width
    else:
        result['font_width'] = effects.font_width
    if effects.font_height == 0:
        result['font_height'] = theme.font_height
    else:
        result['font_height'] = effects.font_height
    if effects.font_thickness == 0:
        result['font_thickness'] = theme.font_thickness
    else:
        result['font_thickness'] = effects.font_thickness
    if effects.font_style == 0:
        result['font_style'] = theme.font_style
    else:
        result['font_style'] = effects.font_style
    if len(effects.justify) == 0:
        if len(theme.justify) == 0:
            result['justify'] = [Justify.CENTER]
        else:
            result['justify'] = theme.justify
    else:
        result['justify'] = effects.justify
    if effects.hidden:
        result['hidden'] = theme.hidden
    else:
        result['hidden'] = effects.hidden
    return TextEffects(**result)


def _merge_stroke(stroke: StrokeDefinition | None, theme: StrokeDefinition) -> Dict[str, Any]:
    if not stroke:
        return {'width': theme.width, 'color': theme.color,
                'type': theme.stroke_type}
    result: Dict[str, Any] = {}
    if stroke.width == 0:
        result['width'] = theme.width
    else:
        result['width'] = stroke.width
    if stroke.color == rgb(0, 0, 0, 0):
        result['color'] = theme.color
    else:
        result['color'] = stroke.color
    if stroke.stroke_type == '':
        result['type'] = theme.stroke_type
    else:
        result['type'] = stroke.stroke_type
    return result


class SchemaPlot(AbstractParser):
    """Plot the schema and write events to plotter base"""

    def __init__(self, file: IO, width: float, height: float, dpi: int,
                 scale:  float = 3.543307, theme: str = 'kicad2000',
                 child: AbstractParser | None = None):
        super().__init__(child)
        self.plotter = Registry().PLOTTER(file, width, height, dpi, scale)  # type: ignore
        self.theme = themes[theme]
        self.library_symbols: Dict[str,  LibrarySymbol] = {}

#    @staticmethod
#    def _transform(symbol: Symbol, path):
#        mirror = "".join(list(symbol.mirror))
#        theta = np.deg2rad(-symbol.angle)
#        trans = np.reshape(MIRROR[mirror], (2, 2)).T
#        rot = np.array([[np.cos(theta), -np.sin(theta)],
#                        [np.sin(theta), np.cos(theta)]])
#
#        verts = np.matmul(np.array(path), rot)
#        verts = np.matmul(verts, trans)
#        verts = (symbol.pos + verts)
#        verts = np.round(verts, 3)
#        return verts

    @staticmethod
    def _scale(pts: PTS_T, scale: float) -> PTS_T:
        return pts * np.array([scale, scale])

    def _drawPolyline(self, symbol: Symbol, polyline: Polyline) -> None:
        _polyline = deepcopy(polyline)
        _polyline.points = transform(symbol, np.array(_polyline.points))

        theme = cast(StrokeDefinition, self.theme['component_outline'])
        stroke = _merge_stroke(_polyline.stroke_definition, theme)
        self.plotter.polyline(
            _polyline.points, stroke['width'], stroke['color'])

    def _drawRectangle(self, symbol: Symbol, rectangle: Rectangle) -> None:
        pts = transform(symbol, ((rectangle.start_x, rectangle.start_y),
                                 (rectangle.end_x, rectangle.end_y)))

        theme = cast(StrokeDefinition, self.theme['component_outline'])
        stroke = _merge_stroke(rectangle.stroke_definition, theme)
        self.plotter.rectangle(
            (pts[0]), (pts[1]), stroke['width'], stroke['color'])

    def _drawCircle(self, symbol: Symbol, circle: Circle) -> None:
        _circle = deepcopy(circle)
        _circle.center = np.array(symbol.pos) + \
            np.array(_circle.center)  # type: ignore

        self.plotter.circle(circle.center, circle.radius,
                            circle.stroke_definition.width, circle.stroke_definition.color)

    def _drawPin(self, symbol: Symbol, pin: Pin) -> None:
        pin_pos = np.array(pin.pos)
        pin_line = transform(symbol,
                             (pin_pos, (pin_pos[0] + (np.cos(math.radians(pin.angle)) * pin.length),
                                        pin_pos[1] + (np.sin(math.radians(pin.angle)) * pin.length))))
        number_pos = transform(symbol,
                               (pin_pos[0] + (np.cos(math.radians(pin.angle)) * pin.length / 2),
                                pin_pos[1] + (np.sin(math.radians(pin.angle)) * pin.length / 2)))

        name_pos = transform(symbol,
                             (pin_pos[0] + (np.cos(math.radians(pin.angle)) * (pin.length + 1)),
                              pin_pos[1] + (np.sin(math.radians(pin.angle)) * (pin.length + 1))))

        stroke = _merge_stroke(None, cast(StrokeDefinition, self.theme['pin']))
        self.plotter.line(pin_line, stroke['width'], stroke['color'])

        number_effects = _merge_text_effects(pin.number[1],
                                             cast(TextEffects, self.theme['pin_number']))
        name_effects = _merge_text_effects(pin.name[1],
                                           cast(TextEffects, self.theme['pin_name']))

        assert symbol.library_symbol, 'symbol must have a library.'
        if (not number_effects.hidden and
            not symbol.library_symbol.pin_numbers_hide and
                symbol.library_symbol.extends != 'power'):
            self.drawText(number_pos, pin.number[0], 0, number_effects)

        if (not name_effects.hidden and
            not symbol.library_symbol.pin_names_hide and
                symbol.library_symbol.extends != 'power' and
                pin.name[0] != '~'):
            self.drawText(name_pos, pin.name[0], 0, name_effects)

    def drawProperty(self, symbol: Symbol, prop: Property):
        effects = _merge_text_effects(
                prop.text_effects, cast(TextEffects, self.theme['text_effects']))
        text = symbol.reference() if prop.key == "Reference" else prop.value
        print(f'value for {prop.key} : {text}')
        self.plotter.text(prop.pos, text, effects.font_height,
                          effects.font_width, effects.face, 0,
                          " ".join(effects.font_style), effects.font_thickness,
                          rgb(0, 0, 0, 1), effects.justify)

    def drawText(self, pos: POS_T, text: str, angle: float, effects: TextEffects):
        _effects = _merge_text_effects(effects, cast(
            TextEffects, self.theme['text_effects']))
        if not effects.hidden:
            self.plotter.text(pos, text, _effects.font_height,
                              _effects.font_width, _effects.face, angle,
                              " ".join(
                                  _effects.font_style), _effects.font_thickness,
                              rgb(0, 0, 0, 1), _effects.justify)

    def start(self, version: str, identifier: str, generator: str,
              paper: str, title_block: TitleBlock):

        self.plotter.start()
        stroke = _merge_stroke(None, cast(StrokeDefinition,
                                          cast(Dict, self.theme['border'])['line']))
        self.plotter.rectangle((.0, .0), (297.0, 210.0),
                               stroke['width'], stroke['color'])
        self.plotter.rectangle(
            (5.0, 5.0), (292.0, 205.0), stroke['width'], stroke['color'])
        self.plotter.rectangle(
            (200.0, 180.0), (292.0, 205.0), stroke['width'], stroke['color'])

        effects = _merge_text_effects(None, cast(TextEffects,
                                                 cast(Dict, self.theme['border'])['comment_1']))
        self.plotter.text((201, 194), title_block.title, effects.font_height,
                          effects.font_width, effects.face, 0,
                          " ".join(effects.font_style), effects.font_thickness,
                          rgb(0, 0, 0, 1), effects.justify)
        self.plotter.text((201, 194), title_block.title, effects.font_height,
                          effects.font_width, effects.face, 0,
                          " ".join(effects.font_style), effects.font_thickness,
                          rgb(0, 0, 0, 1), effects.justify)

        effects = _merge_text_effects(None, cast(TextEffects,
                                                 cast(Dict, self.theme['border'])['comment_3']))
        if 4 in title_block.comment:
            self.plotter.text((201, 182), title_block.comment[4], effects.font_height,
                              effects.font_width, effects.face, 0,
                              " ".join(
                                  effects.font_style), effects.font_thickness,
                              rgb(0, 0, 0, 1), effects.justify)
        if 3 in title_block.comment:
            self.plotter.text((201, 185), title_block.comment[3], effects.font_height,
                              effects.font_width, effects.face, 0,
                              " ".join(
                                  effects.font_style), effects.font_thickness,
                              rgb(0, 0, 0, 1), effects.justify)
        if 2 in title_block.comment:
            self.plotter.text((201, 188), title_block.comment[2], effects.font_height,
                              effects.font_width, effects.face, 0,
                              " ".join(
                                  effects.font_style), effects.font_thickness,
                              rgb(0, 0, 0, 1), effects.justify)
        if 1 in title_block.comment:
            self.plotter.text((201, 191), title_block.comment[1], effects.font_height,
                              effects.font_width, effects.face, 0,
                              " ".join(
                                  effects.font_style), effects.font_thickness,
                              rgb(0, 0, 0, 1), effects.justify)

        super().start(version, identifier, generator, paper, title_block)

    def end(self):
        self.plotter.end()
        super().end()

#    def startSheetInstances(self):
#        super().startSheetInstances()
#
#    def endSheetInstances(self):
#        super().endSheetInstances()
#
#    def startSymbolInstances(self):
#        super(),startSymbolInstances()
#
#    def endSymbolInstances(self):
#        super().endSymbolInstances()

    def visitWire(self, wire: Wire):
        stroke = _merge_stroke(wire.stroke_definition, cast(
            StrokeDefinition, self.theme['wire']))
        self.plotter.line(wire.pts, stroke['width'], stroke['color'])
        super().visitWire(wire)

    def visitJunction(self, junction: Junction):
        stroke = _merge_stroke(None, cast(
            StrokeDefinition, self.theme['wire']))
        self.plotter.circle(junction.pos, 0.4,
                            stroke['width'], stroke['color'], stroke['color'])
        super().visitJunction(junction)

    def visitNoConnect(self, no_connect: NoConnect):
        stroke = _merge_stroke(None, cast(
            StrokeDefinition, self.theme['no_connect']))
        cross = no_connect.pos + \
            np.array([((-0.6, 0.6), (0.6, -0.6)), ((0.6, 0.6), (-0.6, -0.6))])
        self.plotter.line(cross[0], stroke['width'], stroke['color'])
        self.plotter.line(cross[1], stroke['width'], stroke['color'])
        super().visitNoConnect(no_connect)

    def visitLocalLabel(self, local_label: LocalLabel):
        effects = _merge_text_effects(local_label.text_effects, cast(TextEffects,
                                                                     self.theme['local_label']))
        self.plotter.text(local_label.pos, local_label.text, effects.font_height,
                          effects.font_width, effects.face, local_label.angle,
                          " ".join(effects.font_style), effects.font_thickness,
                          rgb(0, 0, 0, 1), effects.justify)
        super().visitLocalLabel(local_label)

    def visitGlobalLabel(self, global_label: GlobalLabel):
        effects = _merge_text_effects(global_label.text_effects, cast(TextEffects,
                                                                      self.theme['local_label']))
        self.plotter.text(global_label.pos, global_label.text, effects.font_height,
                          effects.font_width, effects.face, 0,
                          " ".join(effects.font_style), effects.font_thickness,
                          rgb(0, 0, 0, 1), effects.justify)
        super().visitGlobalLabel(global_label)

#    def visitGraphicalLine(self, graphical_line: GraphicalLine):
#        pass
#
#    def visitGraphicalText(self, graphical_text: GraphicalText):
#        pass
#
#    def visitHierarchicalSheet(self, hierarchical_sheet: HierarchicalSheet):
#        pass

    def visitSymbol(self, symbol: Symbol):
        assert symbol.library_identifier in self.library_symbols, 'library symbol is not set'
        sym = self.library_symbols[symbol.library_identifier]
        for subsym in sym.units:
            if isUnit(subsym, symbol.unit):
                for draw in subsym.graphics:
                    if isinstance(draw, Polyline):
                        self._drawPolyline(symbol, draw)
                    elif isinstance(draw, Rectangle):
                        self._drawRectangle(symbol, draw)
                    elif isinstance(draw, Arc):
                        pass  # TODO self._drawArc(symbol, draw)
                    elif isinstance(draw, Circle):
                        self._drawCircle(symbol, draw)
                    else:
                        print(f"unknown graph type: {draw}")

                for pin in subsym.pins:
                    self._drawPin(symbol, pin)

        # Add the visible text properties
        for field in symbol.properties:
            if field.text_effects and field.text_effects.hidden:
                continue
            if field.value == "~":
                continue

            angle = symbol.angle + field.angle
            if angle == 360:
                angle = 0
            if angle == 180:
                angle = 0

            _field = deepcopy(field)
            if not _field.text_effects:
                _field.text_effects = TextEffects()
            if symbol.angle + _field.angle == 180:
                if Justify.LEFT in _field.text_effects.justify:
                    _field.text_effects.justify = [Justify.RIGHT]
                elif Justify.RIGHT in _field.text_effects.justify:
                    _field.text_effects.justify = [Justify.LEFT]

            self.drawProperty(symbol, _field)
        super().visitSymbol(symbol)

    def visitLibrarySymbol(self, symbol: LibrarySymbol):
        self.library_symbols[symbol.identifier] = symbol
        super().visitLibrarySymbol(symbol)

#    def visitSheetInstance(self, sheet: HierarchicalSheetInstance):
#        pass
#
#    def visitSymbolInstance(self, symbol: SymbolInstance):
#        pass
