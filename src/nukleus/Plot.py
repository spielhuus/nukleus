import math
from abc import ABC, abstractmethod
from io import BytesIO
from typing import List, Tuple

#import cairo
import cairocffi as cairo
import pangocffi as pango
import pangocairocffi as pangocairo
#
import numpy as np

from .model import (FillType, GlobalLabel, Junction, Justify, LibrarySymbol,
                    LocalLabel, NoConnect, Pin, Polyline, Rectangle,
                    StrokeDefinition, Symbol, TextEffects, rgb)
from .model.SchemaElement import POS_T, PTS_T, SchemaElement
from .model.HierarchicalSheetInstance import HierarchicalSheetInstance
from .model.SymbolInstance import SymbolInstance
from .model.Wire import Wire
from .Schema import Schema
from .Theme import themes

FONT_SCALE = 3
Y_TRANS = np.array([1, -1])

f_coord = lambda arr:  [(np.min(arr[::,0]), np.min(arr[...,1])),
                        (np.max(arr[...,0]), np.max(arr[...,1]))]

class DrawLine:
    def __init__(self, pts: PTS_T, width: float, color: rgb, type: str) -> None:
        self.pts = pts
        self.width = width
        self.color = color
        self.type = type

    def dimension(self):
        return f_coord(np.array(self.pts))

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color.get())
        ctx.set_line_width(self.width)
        ctx.move_to(self.pts[0][0], self.pts[0][1])
        ctx.line_to(self.pts[1][0], self.pts[1][1])
        ctx.stroke_preserve()
        ctx.stroke()


class DrawPolyLine:
    def __init__(self, pts: PTS_T, width: float, color: rgb, type: str, fill: rgb|None=None) -> None:
        self.pts = pts
        self.width = width
        self.color = color
        self.type = type
        self.fill = fill

    def dimension(self):
        return f_coord(np.array(self.pts))

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color.get())
        ctx.set_line_width(self.width)
        ctx.move_to(self.pts[0][0], self.pts[0][1])
        for p in self.pts[1:]:
            ctx.line_to(p[0], p[1])
        ctx.stroke_preserve()
        if self.fill:
            ctx.set_source_rgba(*self.fill.get())
            ctx.fill()
        ctx.stroke()


class DrawRect:
    def __init__(self, pts: PTS_T, width: float, color: rgb, type: str, fill: rgb|None=None) -> None:
        self.pts = pts
        self.width = width
        self.color = color
        self.type = type
        self.fill = fill

    def dimension(self):
        return f_coord(np.array(self.pts))

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color.get())
        ctx.set_line_width(self.width)
        ctx.move_to(self.pts[0][0], self.pts[0][1])
        for p in self.pts[1:]:
            ctx.line_to(p[0], p[1])
        ctx.stroke_preserve()
        if self.fill:
            ctx.set_source_rgba(*self.fill.get())
            ctx.fill()
        ctx.stroke()


class DrawCircle:
    def __init__(self, pos: POS_T, radius, width: float, color: rgb, type: str, fill: rgb|None=None) -> None:
        self.pos = pos
        self.radius = radius
        self.width = width
        self.color = color
        self.type = type
        self.fill = fill

    def dimension(self):
        return [(self.pos[0]-self.radius, self.pos[1]-self.radius), 
                (self.pos[0]+self.radius, self.pos[1]+self.radius)]

    def draw(self, ctx):
        ctx.set_line_width(self.width)
        ctx.set_source_rgba(*self.color.get())
        ctx.arc(self.pos[0], self.pos[1], self.radius, 0, 100)
        ctx.stroke_preserve()
        ctx.fill()
        ctx.stroke()


class DrawText:
    def __init__(self, pos: POS_T, text: str, rotation, font_width, font_height, font_weight, font_thickness, justify, hidden) -> None:
        self.pos = pos
        self.text = text
        self.rotation = rotation
        self.font_width=font_width
        self.font_height=font_height
        self.font_weight=font_weight
        self.font_thickness=font_thickness
        self.justify=justify
        self.hidden=hidden

        x, y = (pos[0], pos[1])
        #        if Justify.CENTER in text_effects.justify:
        #            x_bearing, y_bearing, width, height, x_advance, y_advance = \
        #                self.ctx.text_extents(string)
        #            x = x - (width / 2 + x_bearing)
        #            #y = y - (height / 2 + y_bearing)
        #        elif Justify.RIGHT in text_effects.justify:
        #            x_bearing, y_bearing, width, height, x_advance, y_advance = \
        #                self.ctx.text_extents(string)
        #            x = x - (width + x_bearing)
        #            #y = y - (height + y_bearing)
        #        if Justify.TOP in text_effects.justify:
        #            x_bearing, y_bearing, width, height, x_advance, y_advance = \
        #                self.ctx.text_extents(string)
        #            #x = x - (width / 2 + x_bearing)
        #            y = y - (height + y_bearing)


    def dimension(self):
#        pangoctx = pango.Context()
#        layout = pango.Layout(pangoctx)
#        desc = pango.FontDescription()
#        desc.set_size(960)
#        desc.set_family('JetBrains Mono NL Thin')
#        layout.set_font_description(desc)
#        layout.set_alignment(pango.Alignment.CENTER)
#        #layout.set_markup(f'<span font="2">{self.text}</span>')
#        layout.set_text(self.text)
#        print(f'TEXT SIZE: {layout.get_size()}')

        return []
        #return f_coord(np.array(self.pts))

    def draw(self, ctx):
        # TODO print(f'{self.text} {self.rotation}')
        ctx.save()
        ctx.translate(self.pos[0], self.pos[1])
        layout = pangocairo.create_layout(ctx)
        #layout.set_width(pango.units_from_double(10))
        desc = pango.FontDescription()
        desc.set_size(960)
        desc.set_family('osifont')
        layout.set_font_description(desc)
        layout.set_alignment(pango.Alignment.CENTER)
        #layout.set_markup(f'<span font="2">{self.text}</span>')
        layout.set_text(self.text)
        # TODO print(f'TEXT SIZE: {layout.get_size()}')
        pangocairo.show_layout(ctx, layout)
        #ctx.rotate(self.rotation * math.pi / 180.)
        ctx.restore()

#        ctx.save()
#        ctx.translate(self.pos[0], self.pos[1])
##        print(
##            f"text: {self.text} {self.rotation} {math.radians(self.rotation)} {ctx.get_matrix()}"
##        )
#        ctx.rotate(math.radians(self.rotation))
#        ctx.set_font_size(2)
#        ctx.translate(-(self.pos[0]), -(self.pos[1]))
##        print(
##            f"text: {self.text} {self.rotation} {math.radians(self.rotation)} {ctx.get_matrix()}"
##        )
#        ctx.move_to(self.pos[0], self.pos[1])
#        ctx.show_text(self.text)
#        ctx.stroke()
#        ctx.restore()


class Node:
    def __init__(self, _: SchemaElement, theme: str) -> None:
        pass

    def dimension(self) -> List[float]:
        return []

    def draw(self, _):
        pass


class NodeWire(Node):
    def __init__(self, element: Wire, theme: str) -> None:
        self.line = DrawLine(
            element.pts,
            themes[theme]["no_connect"].width,
            themes[theme]["no_connect"].color,
            themes[theme]["no_connect"].type
        )

    def dimension(self) -> List[float]:
        return self.line.dimension()

    def draw(self, ctx) -> None:
        return self.line.draw(ctx)


class NodeJunction(Node):
    def __init__(self, element: Junction, theme: str) -> None:
        self.circle = DrawCircle(
            element.pos,
            .2,
            themes[theme]["no_connect"].width,
            themes[theme]["no_connect"].color,
            themes[theme]["no_connect"].type
        )

    def dimension(self) -> List[float]:
        return self.circle.dimension()

    def draw(self, ctx) -> None:
        return self.circle.draw(ctx)


class NodeLocalLabel(Node):
    def __init__(self, element: LocalLabel, theme: str) -> None:
        self.text = DrawText(element.pos, element.text, 0, 1.25, 1.25, 'normal', 2, Justify.CENTER, False)

    def dimension(self) -> List[float]:
        return self.text.dimension()

    def draw(self, ctx) -> None:
        return self.text.draw(ctx)


class NodeGlobalLabel(Node):
    def __init__(self, element: GlobalLabel, theme: str) -> None:
        self.text = DrawText(element.pos, element.text, 0, 1.25, 1.25, 'normal', 2, Justify.CENTER, False)

    def dimension(self) -> List[float]:
        return self.text.dimension()

    def draw(self, ctx) -> None:
        return self.text.draw(ctx)


class NodeNoConnect(Node):
    def __init__(self, element: NoConnect, theme: str) -> None:
        width = themes[theme]["no_connect"].width
        color = themes[theme]["no_connect"].color
        type = themes[theme]["no_connect"].type
        o: float = 0.5
        self.lines = [
            DrawLine(
                (element.pos + np.array([o, -o]), element.pos + np.array([-o, o])),
                width,
                color,
                type,
            ),
            DrawLine(
                (element.pos + np.array([o, -o]), element.pos + np.array([-o, o])),
                width,
                color,
                type,
            ),
        ]

    def dimension(self) -> List[float]:
        return [] #res

    def draw(self, ctx):
        [x.draw(ctx) for x in self.lines]


class NodeSymbol(Node):
    def __init__(self, element: Symbol, theme: str) -> None:
        self.graphs = []
        self.lines= []
        self.texts = []
        assert element.library_symbol, 'library symbol is not set'
        sym = element.library_symbol
        single_unit = False
        for subsym in sym.units:
            unit = int(subsym.identifier.split("_")[-2])
            # Why does this work here, see Spice.py
            # TODO entity 0 is commonn for all subsyms
            single_unit = False if unit != 0 else True
            if unit == 0 or unit == element.unit or single_unit:
                for draw in subsym.graphics:
                    sd = themes[theme]['component_outline']
#                        draw.stroke_definition,
#                        theme["component_outline"],
#                    )
                    fill = None
                    if draw.fill == FillType.BACKGROUND:
                        fill = themes[theme]["component_body"]
                    elif draw.fill == FillType.FOREGROUND:
                        fill = themes[theme]["component_outline"].color
                    if isinstance(draw, Polyline):
                        self.graphs.append(DrawPolyLine(
                            element._pos(draw.points),
                            width=sd.width,
                            color=sd.color,
                            type=sd.type,
                            fill=fill,
                        ))
                    elif isinstance(draw, Rectangle):
                        verts = [
                            (draw.start_x, draw.start_y),
                            (draw.start_x, draw.end_y),
                            (draw.end_x, draw.end_y),
                            (draw.end_x, draw.start_y),
                            (draw.start_x, draw.start_y),
                        ]
                        self.graphs.append(DrawPolyLine(
                            element._pos(verts),
                            width=sd.width,
                            color=sd.color,
                            type=sd.type,
                            fill=fill,
                        ))
#
#                #            #             if isinstance(draw, DrawArc):
#                #            #                 print("draw arc")
#                #            #                 dp = np.array([draw.x, draw.y])
#                #            #                 pl.arc(dp, draw.r, draw.start * 0.1, draw.end * 0.1,
#                #            #                        linewidth, edgecolor, facecolor)
#                #
#                #            #             elif isinstance(draw, DrawCircle):
#                #            #                 dp = np.array([draw.x, draw.y])
#                #            #                 pl.circle(dp, draw.r, linewidth, edgecolor, facecolor)
#                #
                    else:
                        print(f"unknown graph type: {draw}")
#                #
#        self.pos = element.pos
                for pin in subsym.pins:
                    if pin.length:
                        sd = themes[theme]["pin"]
                        pp = pin._pos()
                        self.lines.append(DrawLine(
                            element._pos(pp),
                            width=sd.width,
                            color=sd.color,
                            type=sd.type,
                        ))

                    if (
                        not sym.pin_numbers_hide
                        and not sym.extends == "power"
                    ):

                        o = np.array(((0, 0.1), (0.1, 0)))
                        o[0] = -abs(o[0])
                        o[1] = abs(o[1])

                        pp = element._pos(pin._pos())
                        self.texts.append(DrawText((pp + o)[0], pin.number[0], 0, 1.25, 1.25, 'normal', 2, Justify.CENTER, False))

                    if (
                        pin.name[0] != "~"
                        and not pin.hidden
                        and not sym.extends == "power"
                    ):

                        pp = element._pos(pin._pos())
                        name_position = pp[1] + sym.pin_names_offset
                        self.texts.append(DrawText(name_position, pin.name[0], 0, 1.25, 1.25, 'normal', 2, Justify.CENTER, False))

        # Add the visible text properties
        for field in element.properties:
            if field.text_effects and field.text_effects.hidden:
                continue
            if field.value == "~":
                continue

            angle = element.angle - field.angle
#            print(
#                f"FIELD ANGLE: {field.value} {field.angle} {element.angle} {angle}"
#            )
            if angle >= 180:
                angle -= 180
            elif angle == 90:
                angle = 270
            self.texts.append(DrawText(field.pos, field.value, angle, 1.25, 1.25, 'normal', 2, Justify.CENTER, False))

    def dimension(self) -> List[float]:
        pts = []
        for graph in self.graphs:
            pts.append(graph.dimension())
        for line in self.lines:
            pts.append(line.dimension())
        #for text in self.texts:
        #    pts.append(text.dimension())
        return f_coord(np.array(pts))

    def draw(self, ctx):
        [x.draw(ctx) for x in self.graphs]
        [x.draw(ctx) for x in self.lines]
        [x.draw(ctx) for x in self.texts]


class ElementFactory:
    def __init__(self, schema: Schema, theme: str = "kicad2000"):
        self._creators = {Wire: NodeWire, Junction: NodeJunction, LocalLabel: NodeLocalLabel, GlobalLabel: NodeGlobalLabel, NoConnect: NodeNoConnect, Symbol: NodeSymbol}
        self.nodes = []
        for element in schema.elements:
            creator = self._creators.get(type(element))
            if creator:
                self.nodes.append(creator(element, theme))
            elif not isinstance(element, (LibrarySymbol, SymbolInstance, HierarchicalSheetInstance)):
                print(f'element not found {type(element)}')


    def dimension(self) -> List[float]:
        coords = []
        for node in self.nodes:
            node_coords = node.dimension()
            if len(node_coords) == 2:
                coords.append(node_coords)
        return f_coord(np.array(coords))
            
    def draw(self, ctx) -> None:
        [x.draw(ctx) for x in self.nodes]


class PlotContext:
    def __init__(self, buffer, width: int, height: int, img_type: str):
        self.sfc = cairo.SVGSurface(buffer, width * 2.54, height * 2.54)  # TODO
        self.ctx = cairo.Context(self.sfc)
        self.ctx.scale(72 / 25.4, 72 / 25.4)  # TODO
        self.ctx.select_font_face(
            "Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL
        )

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.ctx.fill()
        self.sfc.finish()
        self.sfc.flush()


def plot(schema: Schema):
    factory = ElementFactory(schema)
    with PlotContext('schema.svg', 297, 210, 'svg') as ctx:
        factory.draw(ctx.ctx)

#
#
#
#
#
#
#
# class PlotContext:
#    def __init__(self, buffer, width: int, height: int, img_type:str):
#        self.sfc = cairo.SVGSurface(buffer, width * 2.54, height * 2.54)  # TODO
#        self.ctx = cairo.Context(self.sfc)
#        self.ctx.scale(72 / 25.4, 72 / 25.4)  # TODO
#        self.ctx.select_font_face(
#            "Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL
#        )
#
#    def __enter__(self):
#        return self
#
#    def __exit__(self, type, value, traceback):
#        self.ctx.fill()
#        self.sfc.finish()
#        self.sfc.flush()
#
#    def line(
#        self,
#        pts: List[Tuple[float, float]],
#        width: float = 1,
#        color: rgb = rgb(1, 0, 0, 1),
#        fill: rgb | None = None,
#        type: str = "",
#    ):
#
#        print(f"Line {pts} {width} {color} {fill}")
#        self.ctx.set_source_rgba(*color.get())
#        self.ctx.set_line_width(width)
#        self.ctx.move_to(pts[0][0], pts[0][1])
#        for p in pts[1:]:
#            self.ctx.line_to(p[0], p[1])
#        self.ctx.stroke_preserve()
#        if fill:
#            self.ctx.set_source_rgba(*fill.get())
#            self.ctx.fill()
#
#        self.ctx.stroke()
#
#    def arc(
#        self,
#        pts: Tuple[float, float],
#        radius: float,
#        width: float = 1,
#        color: rgb = rgb(0, 0, 0, 0),
#    ):
#
#        self.ctx.set_line_width(width)
#        self.ctx.set_source_rgba(*color.get())
#        self.ctx.arc(pts[0], pts[1], radius, 0, 100)
#        self.ctx.stroke_preserve()
#        self.ctx.fill()
#        self.ctx.stroke()
#
#    def rectangle(
#        self,
#        pts: Tuple[Tuple[float, float], Tuple[float, float]],
#        line_width: float = 1,
#        color: rgb = rgb(0, 0, 0, 0),
#        fill: rgb | None = None,
#        type: str = "",
#    ):
#
#        self.ctx.set_line_width(line_width)
#        self.ctx.set_source_rgba(*color.get())
#        self.ctx.rectangle(
#            pts[0][0], pts[0][1], pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
#        )
#        self.ctx.stroke_preserve()
#        if fill:
#            self.ctx.set_source_rgba(*fill.get())
#            self.ctx.fill_preserve()
#        self.ctx.stroke()
#
#    def text(
#        self,
#        pos: Tuple[float, float],
#        string: str,
#        text_effects: TextEffects,
#        rotation: float = 0,
#    ):
#
#        if not text_effects:
#            text_effects = TextEffects(
#                font_width=1.25,
#                font_height=1.25,
#                font_weight="bold",
#                font_thickness="normal",
#                justify=[Justify.CENTER],
#                hidden=False,
#            )
#
#        print(
#            f"text: {string} {rotation} {math.radians(rotation)} {self.ctx.get_matrix()}"
#        )
#
#        x, y = (pos[0], pos[1])
#        #        if Justify.CENTER in text_effects.justify:
#        #            x_bearing, y_bearing, width, height, x_advance, y_advance = \
#        #                self.ctx.text_extents(string)
#        #            x = x - (width / 2 + x_bearing)
#        #            #y = y - (height / 2 + y_bearing)
#        #        elif Justify.RIGHT in text_effects.justify:
#        #            x_bearing, y_bearing, width, height, x_advance, y_advance = \
#        #                self.ctx.text_extents(string)
#        #            x = x - (width + x_bearing)
#        #            #y = y - (height + y_bearing)
#        #        if Justify.TOP in text_effects.justify:
#        #            x_bearing, y_bearing, width, height, x_advance, y_advance = \
#        #                self.ctx.text_extents(string)
#        #            #x = x - (width / 2 + x_bearing)
#        #            y = y - (height + y_bearing)
#
#        self.ctx.save()
#        self.ctx.translate(x, y)
#        print(
#            f"text: {string} {rotation} {math.radians(rotation)} {self.ctx.get_matrix()}"
#        )
#        self.ctx.rotate(math.radians(rotation))
#        self.ctx.set_font_size(2)
#        self.ctx.translate(-x, -y)
#        print(
#            f"text: {string} {rotation} {math.radians(rotation)} {self.ctx.get_matrix()}"
#        )
#        self.ctx.move_to(x, y)
#        self.ctx.show_text(string)
#        self.ctx.stroke()
#        self.ctx.restore()
#
#    def close(self):
#        self.ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
#        self.ctx.set_line_width(0.02)
#
#
#
# def line(ctx,
#    pts: List[Tuple[float, float]],
#    stroke_definition: StrokeDefinition):
#
#    print(f"Line {pts} {width} {color} {fill}")
#    ctx.set_source_rgba(*color.get())
#    ctx.set_line_width(width)
#    ctx.move_to(pts[0][0], pts[0][1])
#    for p in pts[1:]:
#        ctx.line_to(p[0], p[1])
#    self.ctx.stroke_preserve()
#    if fill:
#        ctx.set_source_rgba(*fill.get())
#        ctx.fill()
#    ctx.stroke()
#
#
# PLOTTER = {
#        'line': lambda context, pts, stroke_definition: StrokeDefinition : {
#            print(f"LLLine {pts} {stroke_definition.color}")
##            self.ctx.set_source_rgba(*stroke_definition.)
##            self.ctx.set_line_width(width)
##            self.ctx.move_to(pts[0][0], pts[0][1])
##            for p in pts[1:]:
##                self.ctx.line_to(p[0], p[1])
##            self.ctx.stroke_preserve()
##            if fill:
##                self.ctx.set_source_rgba(*fill.get())
##                self.ctx.fill()
##
##            self.ctx.stroke()
#        }
# }
#
#
#
# def _get_default_stroke(element: StrokeDefinition, theme: StrokeDefinition):
#    if element.width == 0:
#        element.width = theme.width
#    if element.type == "":
#        element.type == theme.type
#    if element.color == rgb(0, 0, 0, 0):
#        element.color = theme.color
#    return element
#
#
# class Plot:
#    def plot(self, schema: Schema, img_type: str = 'svg') -> BytesIO:
#        theme = themes["kicad2000"]
#        fig_width_mm = 297  # A4 page
#        fig_height_mm = 210
#        inches_per_mm = 1 / 25.4  # Convert cm to inches
#        fig_width = fig_width_mm * inches_per_mm  # width in inches
#        fig_height = fig_height_mm * inches_per_mm  # height in inches
#        svgio = BytesIO()
#
#        with PlotContext(svgio, fig_width_mm, fig_height_mm, img_type) as plot:
#            plot.rectangle([(0, 0), (fig_width_mm, fig_height_mm)])
#            for element in schema.elements:
#                print(element)
#                if isinstance(element, Wire):
#                    sd = _get_default_stroke(element.stroke_definition, theme["wire"])
#                    plot.line(element.pts, width=sd.width, color=sd.color, type=sd.type)
#
#                elif isinstance(element, NoConnect):
#                    o = 0.5
#                    sd = theme["no_connect"]
#                    PLOTTER['line'](plot,
#                        [
#                            element.pos + np.array([-o, -o]),
#                            element.pos + np.array([o, o]),
#                        ], StrokeDefinition())
#
##                    plot.line(
##                        [
##                            element.pos + np.array([-o, -o]),
##                            element.pos + np.array([o, o]),
##                        ],
##                        width=sd.width,
##                        color=sd.color,
##                        type=sd.type,
##                    )
##                    plot.line(
##                        [
##                            element.pos + np.array([o, -o]),
##                            element.pos + np.array([-o, o]),
##                        ],
##                        width=sd.width,
##                        color=sd.color,
##                        type=sd.type,
##                    )
#
#                elif isinstance(element, Junction):
#                    sd = theme["wire"]
#                    plot.arc(element.pos, 0.5, width=sd.width, color=sd.color)
#
#                elif isinstance(element, LocalLabel) or isinstance(
#                    element, GlobalLabel
#                ):
#                    plot.text(
#                        element.pos,  # element.mirror,
#                        element.text,
#                        element.text_effects,
#                        element.angle,
#                    )
#
#                elif isinstance(element, Symbol):
#                    # TODO theta = np.deg2rad(element.angle)
#                    sym = schema.getSymbol(element.library_identifier)
#                    single_unit = False
#                    for subsym in sym.units:
#                        unit = int(subsym.identifier.split("_")[-2])
#                        # Why does this work here, see Spice.py
#                        single_unit = False if unit != 0 else True
#                        if unit == 0 or unit == element.unit or single_unit:
#                            for draw in subsym.graphics:
#                                sd = _get_default_stroke(
#                                    draw.stroke_definition,
#                                    theme["component_outline"],
#                                )
#                                fill = None
#                                if draw.fill == FillType.BACKGROUND:
#                                    fill = theme["component_body"]
#                                elif draw.fill == FillType.FOREGROUND:
#                                    fill = theme["component_outline"].color
#
#                                if isinstance(draw, Polyline):
#                                    plot.line(
#                                        element._pos(draw.points),
#                                        width=sd.width,
#                                        color=sd.color,
#                                        type=sd.type,
#                                        fill=fill,
#                                    )
#                                elif isinstance(draw, Rectangle):
#                                    verts = [
#                                        (draw.start_x, draw.start_y),
#                                        (draw.start_x, draw.end_y),
#                                        (draw.end_x, draw.end_y),
#                                        (draw.end_x, draw.start_y),
#                                        (draw.start_x, draw.start_y),
#                                    ]
#                                    plot.line(
#                                        element._pos(verts),
#                                        width=sd.width,
#                                        color=sd.color,
#                                        type=sd.type,
#                                        fill=fill,
#                                    )
#
#                            #            #             if isinstance(draw, DrawArc):
#                            #            #                 print("draw arc")
#                            #            #                 dp = np.array([draw.x, draw.y])
#                            #            #                 pl.arc(dp, draw.r, draw.start * 0.1, draw.end * 0.1,
#                            #            #                        linewidth, edgecolor, facecolor)
#                            #
#                            #            #             elif isinstance(draw, DrawCircle):
#                            #            #                 dp = np.array([draw.x, draw.y])
#                            #            #                 pl.circle(dp, draw.r, linewidth, edgecolor, facecolor)
#                            #
#                            #                                else:
#                            #                                    print(f"unknown graph type: {draw}")
#                            #
#                            for pin in subsym.pins:
#                                if pin.length:
#                                    sd = theme["pin"]
#                                    pp = pin._pos()
#                                    plot.line(
#                                        element._pos(pp),
#                                        width=sd.width,
#                                        color=sd.color,
#                                        type=sd.type,
#                                    )
#
#                                if (
#                                    not sym.pin_numbers_hide
#                                    and not sym.extends == "power"
#                                ):
#
#                                    o = np.array(((0, 0.1), (0.1, 0)))
#                                    o[0] = -abs(o[0])
#                                    o[1] = abs(o[1])
#
#                                    pp = element._pos(pin._pos())
#
#                                    plot.text((pp + o)[0], pin.number[0], pin.number[1])
#
#                                if (
#                                    pin.name[0] != "~"
#                                    and not pin.hidden
#                                    and not sym.extends == "power"
#                                ):
#
#                                    pp = element._pos(pin._pos())
#                                    name_position = pp[1] + sym.pin_names_offset
#                                    plot.text(name_position, pin.name[0], pin.name[1])
#
#                    # Add the visible text properties
#                    for field in element.properties:
#                        if field.text_effects and field.text_effects.hidden:
#                            continue
#                        if field.value == "~":
#                            continue
#
#                        angle = element.angle - field.angle
#                        print(
#                            f"FIELD ANGLE: {field.value} {field.angle} {element.angle} {angle}"
#                        )
#                        if angle >= 180:
#                            angle -= 180
#                        elif angle == 90:
#                            angle = 270
#                        plot.text(field.pos, field.value, field.text_effects, angle)
#
#                elif not isinstance(element, LibrarySymbol):
#                    print(f"unknown element {type(element)}")
#
#        return svgio
#
#
# class PathList:
#    def __init__(self):
#        self.paths = []
#        self.texts = []
#
#    def path(self, path, linewidth, edgecolor, facecolor):
#        self.paths.append((path, linewidth, edgecolor, facecolor))
#
#    def arc(self, offset, radius, start, end, linewidth, edgecolor, facecolor):
#        verts = []
#        codes = []
#
#        d = end - start
#        if d > 180:
#            d -= 360
#        elif d < -180:
#            d += 360
#        d /= 4
#        while abs(d) > 5:
#            d /= 2
#
#        a = start
#        codes.append(Path.MOVETO)
#
#        print("YY", start, end, a)
#
#        while 1:
#            verts.append((math.cos(a * math.pi / 180), math.sin(a * math.pi / 180)))
#            if abs(a - end) < abs(d / 2):
#                break
#            a += d
#            if a > 180:
#                a -= 360
#            elif a < -180:
#                a += 360
#            print("XX", start, end, a)
#            codes.append(Path.LINETO)
#
#        verts = np.array(verts)
#        verts = verts * radius + offset
#        path = Path(verts, codes)
#        self.path(path, linewidth, edgecolor, facecolor)
#
#    def circle(self, offset, radius, linewidth, edgecolor, facecolor):
#        path = Path.circle(offset, radius)
#        self.path(path, linewidth, edgecolor, facecolor)
#
#    def text(self, offset, mirror, angle, text, effects: TextEffects):
#        if not effects:
#            effects = TextEffects(1.25, 1.25, "", "", [Justify.CENTER], False)
#        if not effects.hidden:
#            self.texts.append((offset, mirror, angle, text, effects))
#
#    def on_ax(self, ax, pos, angle, mirror):
#        for offset, text_mirror, text_angle, text, effects in self.texts:
#            x, y = offset * Y_TRANS
#            _angle = text_angle if text_angle <= 180 else text_angle - 180
#            #            if angle >= 180 or angle < 0:
#            #                if halign == 'right':
#            #                    halign = 'left'
#            #                elif halign == 'left':
#            #                    halign = 'right'
#            #                if valign == 'top':
#            #                    valign = 'bottom'
#            #                elif valign == 'bottom':
#            #                    valign = 'top'
#            #                angle -= 180
#
#            kw = {
#                "x": x,
#                "y": y,
#                "color": "black",  # color,
#                # TODO 'font': 'sans-serif',
#                "fontsize": (1.25 if effects.font_height == 0 else effects.font_height)
#                * FONT_SCALE,
#                "s": text,
#                "rotation": _angle,
#                "rotation_mode": "anchor",
#                "horizontalalignment": Justify.halign(effects.justify),
#                "verticalalignment": Justify.valign(effects.justify),
#                "clip_on": True,
#            }
#
#            ax.text(**kw)
#
#        if self.paths:
#            d = {}
#            d["paths"] = []
#            d["linewidths"] = []
#            d["edgecolors"] = []
#            d["facecolors"] = []
#
#            for path, linewidth, edgecolor, facecolor in self.paths:
#                verts = _pos(pos, path.vertices, angle, mirror)
#                verts = np.array(verts * Y_TRANS)
#                path.vertices = verts
#                d["paths"].append(path)
#                d["linewidths"].append(linewidth)
#                d["edgecolors"].append(edgecolor)
#                d["facecolors"].append(facecolor)
#
#            pc = PathCollection(**d)
#            ax.add_collection(pc)
#
#
# def plot(fig, ax, sch: Schema, base_width: float = 0.1, edge_color="brown"):
#
#    WIDTH, HEIGHT = 256, 256
#
#    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
#    ctx = cairo.Context(surface)
#
#    ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas
#
#    pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
#    pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
#    pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity
#
#    ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
#    ctx.set_source(pat)
#    ctx.fill()
#
#    ctx.translate(0.1, 0.1)  # Changing the current transformation matrix
#
#    ctx.move_to(0, 0)
#    # Arc(cx, cy, radius, start_angle, stop_angle)
#    ctx.arc(0.2, 0.1, 0.1, -math.pi / 2, 0)
#    ctx.line_to(0.5, 0.1)  # Line to (x,y)
#    # Curve(x1, y1, x2, y2, x3, y3)
#    ctx.curve_to(0.5, 0.2, 0.5, 0.4, 0.2, 0.8)
#    ctx.close_path()
#
#    ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
#    ctx.set_line_width(0.02)
#    ctx.stroke()
#
#    surface.write_to_png("example.png")  # Output to png
#
#
##    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
##    ctx = cairo.Context(surface)
##
##    wires = []
##    noconns = []
##    conns = []
##    notes = []
##
##    print(fig.get_size_inches())
##    width, height = fig.get_size_inches()*fig.dpi
##    ax.set_xlim(0, width) * 2
##    ax.set_ylim(0, height) * 2
##    #print("Dot per inch(DPI) for the figure is: ", fig.dpi)
##    #bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
##    #width, height = bbox.width, bbox.height
##    print("Axis sizes are(in pixels):", width, height)
##    pl = PathList()
##    pl.path(Path([(-1000, -1000), (width, -1000), (width, height), (-1000, height), (-1000, -1000)]),
##            1,
##            edge_color,
##            'red')
##    pl.on_ax(ax, (0, 0), 0, '')
##
##    for element in sch.elements:
##        if isinstance(element, Wire):
##            wires.append(np.array(element.pts * Y_TRANS))
##        elif isinstance(element, NoConnect):
##            o = 0.5
##            xy = (element.pos * Y_TRANS)
##            noconns.append([xy + (-o, -o), xy + (o, o)])
##            noconns.append([xy + (o, -o), xy + (-o, o)])
##        elif isinstance(element, Junction):
##            xy = (element.pos * Y_TRANS)
##            conns.append(xy)
##        elif isinstance(element, LocalLabel) or isinstance(element, GlobalLabel):
##            pl = PathList()
##            pl.text(element.pos, '',  # element.mirror,
##                    element.angle,
##                    element.text,
##                    element.text_effects)
##            pl.on_ax(ax, element.pos, element.angle, '')
##
##        elif isinstance(element, Symbol):
##            sym = sch.getSymbol(element.library_identifier)
##            pl = PathList()
##            single_unit = False
##            for subsym in sym.units:
##                unit = int(subsym.identifier.split('_')[-2])
##                # Why does this work here, see Spice.py
##                single_unit = False if unit != 0 else True
##                if unit == 0 or unit == element.unit or single_unit:
##                    for draw in subsym.graphics:
##                        linewidth = base_width
##                        # if draw.thickness:
##                        #    linewidth *= draw.thickness / 10
##
##                        edgecolor = 'brown'
##                        if draw.fill == FillType.BACKGROUND:
##                            facecolor = 'yellow'
##                        elif draw.fill == FillType.FOREGROUND:
##                            facecolor = 'brown'
##                        else:
##                            facecolor = 'none'
##
##                        if isinstance(draw, Polyline):
##                            verts = draw.points
##                            pl.path(Path(verts),
##                                    base_width if
##                                    draw.stroke_definition.width == 0
##                                    else draw.stroke_definition.width,
##                                    edgecolor,
##                                    facecolor)
##
##                        elif isinstance(draw, Rectangle):
##                            verts = [
##                                (draw.start_x, draw.start_y),
##                                (draw.start_x, draw.end_y),
##                                (draw.end_x, draw.end_y),
##                                (draw.end_x, draw.start_y),
##                                (draw.start_x, draw.start_y)]
##                            pl.path(Path(verts), linewidth,
##                                    edgecolor, facecolor)
##
##    #             if isinstance(draw, DrawArc):
##    #                 print("draw arc")
##    #                 dp = np.array([draw.x, draw.y])
##    #                 pl.arc(dp, draw.r, draw.start * 0.1, draw.end * 0.1,
##    #                        linewidth, edgecolor, facecolor)
##
##    #             elif isinstance(draw, DrawCircle):
##    #                 dp = np.array([draw.x, draw.y])
##    #                 pl.circle(dp, draw.r, linewidth, edgecolor, facecolor)
##
##                        else:
##                            print(f"unknown graph type: {draw}")
##
##                    for pin in subsym.pins:
##                        if pin.length:
##                            pp = _pin_pos(pin)
##                            pl.path(Path(
##                                pp),
##                                base_width,
##                                edgecolor, facecolor)
##
##                        #if not sym.pin_numbers_hide \
##                        #   and not symedgecolor.extends == 'power': TODO
##                        theta = np.deg2rad(element.angle + pin.angle)
##                        rot = np.array([math.cos(theta), math.sin(theta)])
##
##                        o = np.matmul(((0,1),(1,0)), rot)
##                        o[0] = -abs(o[0])
##                        o[1] = abs(o[1])
##                        number_position = \
##                            (pp[1] + (-1, 1)) + element.pos
##                        pl.text(pp[1] + element.pos + o,  # number_position + o,
##                                    '',
##                                    pin.angle,
##                                    f"{pin.number[0]} {element.angle} {pin.angle}",
##                                    pin.number[1])
##
##                        if pin.name[0] != '~' \
##                           and not pin.hidden \
##                           and not sym.extends == 'power':
##                            name_position = \
##                                (pp[1] + sym.pin_names_offset) + element.pos
##                            pl.text(name_position,
##                                    '',
##                                    pin.angle,
##                                    pin.name[0],
##                                    pin.name[1])
##
##            # Add the visible text properties
##            for field in element.properties:
##                if field.text_effects and field.text_effects.hidden:
##                    continue
##                if field.value == '~':
##                    continue
##
##                text_angle = element.angle + field.angle
##                if text_angle == 360:  # TODO
##                    text_angle = 0
##                if text_angle == 180:
##                    text_angle = 0
##                pl.text(field.pos,
##                        element.mirror,
##                        text_angle,
##                        field.value, field.text_effects)
##
##            pl.on_ax(ax, np.array(
##                (element.pos[0], element.pos[1])),
##                element.angle, element.mirror)
##
##    ax.add_collection(LineCollection(
##        wires, linewidths=base_width,
##        colors='green',
##        linestyle='solid'))
##
##    ax.add_collection(LineCollection(noconns, linewidths=base_width,
##                                     colors='red',
##                                     linestyle='solid'))
##
##    conn_ellipses = EllipseCollection(0.8, 0.8, 0,  # 50, 50, 0,
##                                      units='x',
##                                      offsets=conns,
##                                      edgecolor=None,
##                                      facecolor='green',
##                                      transOffset=ax.transData)
##    ax.add_collection(conn_ellipses)
##
##    ax.get_xaxis().set_visible(False)
##    ax.get_yaxis().set_visible(False)
##    ax.axis('equal')
##
##    fig = ax.get_figure()
##    x_scale = fig.bbox_inches.width * ax.get_position().width * 72 / \
##        float(np.diff(ax.get_xlim()))
##    y_scale = fig.bbox_inches.height * ax.get_position().width * 72 / \
##        float(np.diff(ax.get_ylim()))
##    # scale_ax(ax, min(x_scale, y_scale) * 16)
