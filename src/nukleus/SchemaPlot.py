from typing import IO, Any, Dict, cast, List

import math
from copy import deepcopy

import numpy as np
import shapely
import shapely.geometry

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable

from nukleus.Registry import Registry

from .AbstractParser import AbstractParser
from .ModelBase import Justify, StrokeDefinition, TextEffects, TitleBlock, rgb
from .ModelSchema import (Arc, Circle, GlobalLabel, Junction, LibrarySymbol,
                          LocalLabel, NoConnect, Pin, Polyline, Property,
                          Rectangle, SchemaElement, Symbol, Wire, isUnit)
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
    if effects.color == rgb(0, 0, 0, 0):
        result['color'] = theme.color
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

    def __init__(self, file: IO, width: float, height: float, dpi: int, border: bool = True,
                 scale:  float = 3.543307, theme: str = 'kicad2000',
                 child: AbstractParser | None = None):
        super().__init__(child)
        self.file = file
        self.scale = scale
        self.border = border
        self.offset = (0, 0)
        self.theme = themes[theme]
        self.library_symbols: Dict[str,  LibrarySymbol] = {}
        self.identifier = ''
        self.version = ''
        self.generator = ''
        self.paper = ''
        self.title_block: TitleBlock|None = None
        self.geometry = [] #shapely.geometry.GeometryCollection()
        self.elements: List[SchemaElement] = []

    @staticmethod
    def _scale(pts: PTS_T, scale: float) -> PTS_T:
        return pts * np.array([scale, scale])

    @staticmethod
    def _offset(pts: PTS_T, offset: POS_T) -> POS_T:
        return pts + np.array(offset) # type: ignore

    @staticmethod
    def _pos(pts: PTS_T, offset: POS_T, scale: float) -> PTS_T:
        return SchemaPlot._scale(SchemaPlot._offset(pts, offset), scale)

    @staticmethod
    def _get_text_size(text: str, pos: POS_T, effects: TextEffects, angle: float):
        pointSize = 1
        font = TTFont('/usr/local/share/fonts/TT/osifont.ttf')
        cmap = font['cmap']
        t = cmap.getcmap(3,1).cmap
        s = font.getGlyphSet()
        units_per_em = font['head'].unitsPerEm
        total = 0
        for c in text:
            if ord(c) in t and t[ord(c)] in s:
                total += s[t[ord(c)]].width
            else:
                total += s['.notdef'].width
        total = total*float(pointSize)/units_per_em

        pts = ((pos[0], pos[1]-effects.font_height/2), (pos[0]+total, pos[1]+effects.font_height/2))
        if Justify.RIGHT in effects.justify:
            pts = ((pts[0][0]-total, pts[0][1]), (pts[1][0]-total, pts[1][1]))

        return pts

    def _drawPolyline(self, plotter, symbol: Symbol, polyline: Polyline) -> None:
        pts = transform(symbol, np.array(polyline.points))
        theme = cast(StrokeDefinition, self.theme['component_outline'])
        stroke = _merge_stroke(polyline.stroke_definition, theme)
        plotter.polyline(
            SchemaPlot._pos(pts, self.offset, self.scale),
            stroke['width']*self.scale,
            stroke['color'])

    def _drawRectangle(self, plotter, symbol: Symbol, rectangle: Rectangle) -> None:
        pts = transform(symbol, ((rectangle.start_x, rectangle.start_y),
                                 (rectangle.end_x, rectangle.end_y)))
        theme = cast(StrokeDefinition, self.theme['component_outline'])
        stroke = _merge_stroke(rectangle.stroke_definition, theme)
        plotter.rectangle(
            SchemaPlot._pos(pts[0], self.offset, self.scale),
            SchemaPlot._pos(pts[1], self.offset, self.scale),
            stroke['width']*self.scale, stroke['color'])

    def _drawCircle(self, plotter, symbol: Symbol, circle: Circle) -> None:
        center = np.array(symbol.pos) + np.array(circle.center)
        plotter.circle(SchemaPlot._pos(center, self.offset, self.scale),
                       circle.radius*self.scale,
                       circle.stroke_definition.width*self.scale,
                       circle.stroke_definition.color)

    def _drawPin(self, plotter, symbol: Symbol, pin: Pin) -> None:
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
        plotter.line(SchemaPlot._pos(pin_line, self.offset, self.scale),
                     stroke['width']*self.scale, stroke['color'])

        number_effects = _merge_text_effects(
                pin.number[1], cast(TextEffects, self.theme['pin_number']))
        name_effects = _merge_text_effects(
                pin.name[1], cast(TextEffects, self.theme['pin_name']))

        assert symbol.library_symbol, 'symbol must have a library.'
        if (not number_effects.hidden and
            not symbol.library_symbol.pin_numbers_hide and
                symbol.library_symbol.extends != 'power'):
            self.drawText(plotter, SchemaPlot._pos(number_pos, self.offset, self.scale), pin.number[0], 0, number_effects)

        if (not name_effects.hidden and
            not symbol.library_symbol.pin_names_hide and
                symbol.library_symbol.extends != 'power' and
                pin.name[0] != '~'):
            self.drawText(plotter, SchemaPlot._pos(name_pos, self.offset, self.scale), pin.name[0], 0, name_effects)

    def drawProperty(self, plotter, symbol: Symbol, prop: Property):
        effects = _merge_text_effects(
                prop.text_effects, cast(TextEffects, self.theme['text_effects']))
        text = symbol.reference() if prop.key == "Reference" else prop.value
        plotter.text(SchemaPlot._pos(prop.pos, self.offset, self.scale), text, effects.font_height*self.scale,
                          effects.font_width*self.scale, effects.face, 0,
                          " ".join(effects.font_style), effects.font_thickness,
                          effects.color, effects.justify)

    def _property_size(self, symbol: Symbol, prop: Property):
        effects = _merge_text_effects(
                prop.text_effects, cast(TextEffects, self.theme['text_effects']))
        text = symbol.reference() if prop.key == "Reference" else prop.value
        effects = _merge_text_effects(prop.text_effects, cast(TextEffects, self.theme['local_label']))
        return SchemaPlot._get_text_size(text, prop.pos, effects, prop.angle)

    def drawText(self, plotter, pos: POS_T, text: str, angle: float, effects: TextEffects):
        #_effects = _merge_text_effects(effects, cast(
        #    TextEffects, self.theme['text_effects']))
        if not effects.hidden:
            plotter.text(pos, text,
                         effects.font_height*self.scale,
                         effects.font_width*self.scale,
                         effects.face, angle,
                        " ".join(effects.font_style),
                         effects.font_thickness,
                         effects.color,
                         effects.justify)

    def start(self, version: str, generator: str):
        self.version = version
        self.generator = generator
        super().start(version, generator)

    def visitIdentifier(self, identifier: str):
        self.identifier = identifier
        super().visitIdentifier(identifier)

    def visitPaper(self, paper: str):
        self.paper = paper
        super().visitPaper(paper)

    def visitTitleBlock(self, title_block: TitleBlock):
        self.title_block = title_block
        super().visitTitleBlock(title_block)

    def _drawTitleBlock(self, plotter, title_block: TitleBlock):
        stroke = _merge_stroke(None, cast(StrokeDefinition,
                                          cast(Dict, self.theme['border'])['line']))
        plotter.rectangle((.0, .0), self._scale((297.0, 210.0), self.scale),
                               stroke['width'], stroke['color'])
        plotter.rectangle(
            self._scale((5.0, 5.0), self.scale), self._scale((292.0, 205.0), self.scale), stroke['width'], stroke['color'])
        plotter.rectangle(
            self._scale((200.0, 180.0), self.scale), self._scale((292.0, 205.0), self.scale), stroke['width'], stroke['color'])

        effects = _merge_text_effects(None, cast(TextEffects,
                                                 cast(Dict, self.theme['border'])['comment_1']))
        plotter.text(self._scale((201, 194), self.scale), title_block.title, effects.font_height*self.scale,
                          effects.font_width*self.scale, effects.face, 0,
                          " ".join(effects.font_style), effects.font_thickness,
                          rgb(0, 0, 0, 1), effects.justify)
        plotter.text(self._scale((201, 194), self.scale), title_block.title, effects.font_height*self.scale,
                          effects.font_width*self.scale, effects.face, 0,
                          " ".join(effects.font_style), effects.font_thickness,
                          rgb(0, 0, 0, 1), effects.justify)

        effects = _merge_text_effects(None, cast(TextEffects,
                 cast(Dict, self.theme['border'])['comment_3']))

        if 4 in title_block.comment:
            plotter.text(self._scale((201, 182), self.scale), title_block.comment[4], effects.font_height*self.scale,
                              effects.font_width*self.scale, effects.face, 0,
                              " ".join(
                                  effects.font_style), effects.font_thickness,
                              rgb(0, 0, 0, 1), effects.justify)
        if 3 in title_block.comment:
            plotter.text(self._scale((201, 185), self.scale), title_block.comment[3], effects.font_height*self.scale,
                              effects.font_width*self.scale, effects.face, 0,
                              " ".join(
                                  effects.font_style), effects.font_thickness,
                              rgb(0, 0, 0, 1), effects.justify)
        if 2 in title_block.comment:
            plotter.text(self._scale((201, 188), self.scale), title_block.comment[2], effects.font_height*self.scale,
                              effects.font_width*self.scale, effects.face, 0,
                              " ".join(
                                  effects.font_style), effects.font_thickness,
                              rgb(0, 0, 0, 1), effects.justify)
        if 1 in title_block.comment:
            plotter.text(self._scale((201, 191), self.scale), title_block.comment[1], effects.font_height*self.scale,
                              effects.font_width*self.scale, effects.face, 0,
                              " ".join(
                                  effects.font_style), effects.font_thickness,
                              rgb(0, 0, 0, 1), effects.justify)

    def end(self):

        _size = (0, 0)
        if self.border:
            _size = (297, 210)
        else:
            geometry = shapely.geometry.GeometryCollection(self.geometry)
            bounds = geometry.bounds
            self.offset = (bounds[0], bounds[1]) * np.array([-1, -1])
            _size = ((bounds[2]-bounds[0])*self.scale, (bounds[3]-bounds[1])*self.scale)

        print(f'plot(Offset={self.offset}, Size:{_size}, Scale:{self.scale})')

        plotter = Registry().PLOTTER(self.file, _size[0], _size[1], 900, 1)  # type: ignore

        plotter.start()
        #plotter.rectangle((bounds[0], bounds[1]), (bounds[2], bounds[3]), 0.2, rgb(1, 0, 0, 1)) # TODO

        if self.border:
            self._drawTitleBlock(plotter, self.title_block)
        for element in self.elements:
            if isinstance(element, Symbol):
                self._drawSymbol(plotter, element)
            elif isinstance(element, Wire):
                self._drawWire(plotter, element)
            elif isinstance(element, LocalLabel):
                self._drawLocalLabel(plotter, element)
            elif isinstance(element, GlobalLabel):
                self._drawGlobalLabel(plotter, element)
            elif isinstance(element, Junction):
                self._drawJunction(plotter, element)
            elif isinstance(element, NoConnect):
                self._drawNoConnect(plotter, element)

        plotter.end()
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
        self.geometry.append(shapely.geometry.LineString(wire.pts))
        self.elements.append(wire)
        super().visitWire(wire)

    def _drawWire(self, plotter, wire: Wire):
        stroke = _merge_stroke(wire.stroke_definition, cast(
            StrokeDefinition, self.theme['wire']))
        plotter.line(SchemaPlot._pos(wire.pts, self.offset, self.scale),
                stroke['width']*self.scale, stroke['color'])

    def visitJunction(self, junction: Junction):
        self.elements.append(junction)
        super().visitJunction(junction)

    def _drawJunction(self, plotter, junction: Junction):
        stroke = _merge_stroke(None, cast(
            StrokeDefinition, self.theme['wire']))
        plotter.circle(SchemaPlot._pos(junction.pos, self.offset, self.scale), 0.4*self.scale,
                            stroke['width']*self.scale, stroke['color'], stroke['color'])

    def visitNoConnect(self, no_connect: NoConnect):
        self.elements.append(no_connect)
        super().visitNoConnect(no_connect)

    def _drawNoConnect(self, plotter, no_connect: NoConnect):
        stroke = _merge_stroke(None, cast(
            StrokeDefinition, self.theme['no_connect']))
        cross = no_connect.pos + \
            np.array([((-0.6, 0.6), (0.6, -0.6)), ((0.6, 0.6), (-0.6, -0.6))])
        plotter.line(SchemaPlot._pos(cross[0], self.offset, self.scale),
                     stroke['width']*self.scale, stroke['color'])
        plotter.line(SchemaPlot._pos(cross[1], self.offset, self.scale),
                     stroke['width']*self.scale, stroke['color'])

    def visitLocalLabel(self, local_label: LocalLabel):
        self.elements.append(local_label)
        effects = _merge_text_effects(local_label.text_effects, cast(TextEffects, self.theme['local_label']))
        pts = SchemaPlot._get_text_size(local_label.text, local_label.pos, effects, local_label.angle)
        self.geometry.append(shapely.geometry.Polygon([(pts[0][0], pts[0][1]), (pts[1][0], pts[0][1]), (pts[1][0], pts[1][1]), (pts[0][1], pts[1][1]), (pts[0][0], pts[0][1])]))
        super().visitLocalLabel(local_label)

    def _drawLocalLabel(self, plotter, local_label: LocalLabel):
        effects = _merge_text_effects(local_label.text_effects, cast(TextEffects,
                                                                     self.theme['local_label']))
        plotter.text(SchemaPlot._pos(local_label.pos, self.offset, self.scale), local_label.text, effects.font_height*self.scale,
                          effects.font_width*self.scale, effects.face, local_label.angle,
                          " ".join(effects.font_style), effects.font_thickness,
                          rgb(0, 0, 0, 1), effects.justify)

        pts = SchemaPlot._get_text_size(local_label.text, local_label.pos, effects, local_label.angle)
        plotter.rectangle(
            SchemaPlot._pos((pts[0]), self.offset, self.scale), SchemaPlot._pos((pts[1]), self.offset, self.scale), .1, rgb(1,0,0,1))

    def visitGlobalLabel(self, global_label: GlobalLabel):
        self.elements.append(global_label)
        effects = _merge_text_effects(global_label.text_effects, cast(TextEffects, self.theme['local_label']))
        pts = SchemaPlot._get_text_size(global_label.text, global_label.pos, effects, global_label.angle)
        self.geometry.append(shapely.geometry.Polygon([(pts[0][0], pts[0][1]), (pts[1][0], pts[0][1]), (pts[1][0], pts[1][1]), (pts[0][1], pts[1][1]), (pts[0][0], pts[0][1])]))
        super().visitGlobalLabel(global_label)

    def _drawGlobalLabel(self, plotter, global_label: GlobalLabel):
        effects = _merge_text_effects(global_label.text_effects, cast(TextEffects, self.theme['local_label']))
        plotter.text(SchemaPlot._pos(global_label.pos, self.offset, self.scale), global_label.text, effects.font_height*self.scale,
                          effects.font_width*self.scale, effects.face, 0,
                          " ".join(effects.font_style), effects.font_thickness,
                          rgb(0, 0, 0, 1), effects.justify)

#    def visitGraphicalLine(self, graphical_line: GraphicalLine):
#        pass
#
#    def visitGraphicalText(self, graphical_text: GraphicalText):
#        pass
#
#    def visitHierarchicalSheet(self, hierarchical_sheet: HierarchicalSheet):
#        pass

    def visitSymbol(self, symbol: Symbol):
        self.elements.append(symbol)

        if symbol.on_schema:
            assert symbol.library_identifier in self.library_symbols, 'library symbol is not set'
            sym = self.library_symbols[symbol.library_identifier]
            for subsym in sym.units:
                if isUnit(subsym, symbol.unit):
                    for draw in subsym.graphics:
                        if isinstance(draw, Polyline):
#                        if len(draw.points) > 2:
#                            self.geometry.append(shapely.geometry.Polygon(transform(symbol, draw.points)))
#                        else:
                            self.geometry.append(shapely.geometry.LineString(transform(symbol, draw.points)))
                        elif isinstance(draw, Rectangle):
                            self.geometry.append(shapely.geometry.Polygon(transform(symbol, [(draw.start_x, draw.start_x), (draw.end_x, draw.start_y), (draw.end_x, draw.end_y), (draw.start_x, draw.end_y), (draw.start_x, draw.start_y)])))
                        elif isinstance(draw, Arc):
                            self.geometry.append(shapely.geometry.Point(transform(symbol, draw.start)).buffer(2))
                            pass  # TODO self._drawArc(symbol, draw)
                        elif isinstance(draw, Circle):
                            self.geometry.append(shapely.geometry.Point(transform(symbol, draw.center)).buffer(draw.radius))
                        else:
                            print(f"unknown graph type: {draw}")

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

                pts = self._property_size(symbol, _field)
                self.geometry.append(shapely.geometry.Polygon([(pts[0][0], pts[0][1]), (pts[1][0], pts[0][1]), (pts[1][0], pts[1][1]), (pts[0][1], pts[1][1]), (pts[0][0], pts[0][1])]))

        super().visitSymbol(symbol)

    def _drawSymbol(self, plotter, symbol: Symbol):
        if symbol.on_schema:
            assert symbol.library_identifier in self.library_symbols, 'library symbol is not set'
            sym = self.library_symbols[symbol.library_identifier]
            for subsym in sym.units:
                if isUnit(subsym, symbol.unit):
                    for draw in subsym.graphics:
                        if isinstance(draw, Polyline):
#                        if len(draw.points) > 2:
#                            self.geometry.append(shapely.geometry.Polygon(transform(symbol, draw.points)))
#                        else:
                            self._drawPolyline(plotter, symbol, draw)
                        elif isinstance(draw, Rectangle):
                            self._drawRectangle(plotter, symbol, draw)
                        elif isinstance(draw, Arc):
                            pass  # TODO self._drawArc(symbol, draw)
                        elif isinstance(draw, Circle):
                            self._drawCircle(plotter, symbol, draw)
                        else:
                            print(f"unknown graph type: {draw}")

                    for pin in subsym.pins:
                        self._drawPin(plotter, symbol, pin)

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

                self.drawProperty(plotter, symbol, _field)

    def visitLibrarySymbol(self, symbol: LibrarySymbol):
        self.library_symbols[symbol.identifier] = symbol
        super().visitLibrarySymbol(symbol)

#    def visitSheetInstance(self, sheet: HierarchicalSheetInstance):
#        pass
#
#    def visitSymbolInstance(self, symbol: SymbolInstance):
#        pass
