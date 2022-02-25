from io import BytesIO
from typing import List, IO

import cairo
from gi.repository import Pango
from gi.repository import PangoCairo

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

f_coord = lambda arr:  [(np.min(arr[...,0]), np.min(arr[...,1])),
                        (np.max(arr[...,0]), np.max(arr[...,1]))]

class DrawLine:
    def __init__(self, pts: PTS_T, width: float, color: rgb, type: str) -> None:
        self.pts = pts
        self.width = width
        self.color = color
        self.type = type

    def dimension(self, ctx):
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

    def dimension(self, ctx):
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

    def dimension(self, ctx):
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

    def dimension(self, ctx):
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


    def dimension(self, ctx):
        layout = PangoCairo.create_layout(ctx) # TODO pangocairo.create_layout(ctx)
        pctx = layout.get_context()
        desc = Pango.FontDescription()
        desc.set_size(960)
        desc.set_family('osifont')
        layout.set_font_description(desc)
        layout.set_alignment(Pango.Alignment.CENTER)
        fo = cairo.FontOptions()
        fo.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        PangoCairo.context_set_font_options(pctx, fo)
        layout.set_text(self.text)
        size = layout.get_pixel_size()
        return [(self.pos[0], self.pos[1]), (self.pos[0]+size[0], self.pos[1]+size[1])]

    def draw(self, ctx):
        # TODO print(f'{self.text} {self.rotation}')
        ctx.save()
        ctx.translate(self.pos[0], self.pos[1])
        layout = PangoCairo.create_layout(ctx) # TODO pangocairo.create_layout(ctx)
        pctx = layout.get_context()
        #layout.set_width(pango.units_from_double(10))
        desc = Pango.FontDescription()
        desc.set_size(960)
        desc.set_family('osifont')
        layout.set_font_description(desc)
        layout.set_alignment(Pango.Alignment.CENTER)
        #layout.set_markup(f'<span font="2">{self.text}</span>')
        fo = cairo.FontOptions()
        fo.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        PangoCairo.context_set_font_options(pctx, fo)

        layout.set_text(self.text)
        PangoCairo.show_layout(ctx, layout)
        #ctx.rotate(self.rotation * math.pi / 180.)
        
        # TODO remove draw box around text
        size = layout.get_pixel_size()
        ctx.set_source_rgba(*rgb(1, 0, 0, 1).get())
        ctx.set_line_width(0.1)
        ctx.move_to(0, 0)
        ctx.line_to(size[0], 0)
        ctx.line_to(size[0], size[1])
        ctx.line_to(0, size[1])
        ctx.line_to(0, 0)
        ctx.stroke_preserve()
        ctx.stroke()

        ctx.restore()


class Node:
    def __init__(self, _: SchemaElement, theme: str) -> None:
        pass

    def dimension(self, ctx) -> List[float]:
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

    def dimension(self, ctx) -> List[float]:
        return self.line.dimension(ctx)

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

    def dimension(self, ctx) -> List[float]:
        return self.circle.dimension(ctx)

    def draw(self, ctx) -> None:
        return self.circle.draw(ctx)


class NodeLocalLabel(Node):
    def __init__(self, element: LocalLabel, theme: str) -> None:
        self.text = DrawText(element.pos, element.text, 0, 1.25, 1.25, 'normal', 2, Justify.CENTER, False)

    def dimension(self, ctx) -> List[float]:
        return self.text.dimension(ctx)

    def draw(self, ctx) -> None:
        return self.text.draw(ctx)


class NodeGlobalLabel(Node):
    def __init__(self, element: GlobalLabel, theme: str) -> None:
        self.text = DrawText(element.pos, element.text, 0, 1.25, 1.25, 'normal', 2, Justify.CENTER, False)

    def dimension(self, ctx) -> List[float]:
        return self.text.dimension(ctx)

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

    def dimension(self, ctx) -> List[float]:
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

    def dimension(self, ctx) -> List[float]:
        pts = []
        for graph in self.graphs:
            pts.append(graph.dimension(ctx))
        for line in self.lines:
            pts.append(line.dimension(ctx))
        for text in self.texts:
            pts.append(text.dimension(ctx))
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


    def dimension(self, ctx) -> List[float]:
        coords = []
        for node in self.nodes:
            node_coords = node.dimension(ctx)
            if len(node_coords) == 2:
                coords.append(node_coords)

        return f_coord(np.array(coords))

    def draw(self, ctx) -> None:
        [x.draw(ctx) for x in self.nodes]


class PlotContext:
    def __init__(self, buffer, width: int, height: int, image_type: str):
        self.sfc = None
        if image_type == 'pdf':
            self.sfc = cairo.PDFSurface(buffer, width / 25.4 * 72, height / 25.4 * 72)
        else:
            self.sfc = cairo.SVGSurface(buffer, width / 25.4 * 72, height / 25.4 * 72)

        self.ctx = cairo.Context(self.sfc)
        self.ctx.scale(72. / 25.4, 72. / 25.4)  # TODO
        self.ctx.select_font_face(
            "Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL
        )

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.ctx.fill()
        assert self.sfc, 'Image Surface not set.'
        self.sfc.finish()
        self.sfc.flush()


def plot(schema: Schema, out: IO=BytesIO(), image_type='svg') -> IO:
    factory = ElementFactory(schema)
    with PlotContext(out, 297, 210, image_type) as ctx:
        outline = factory.dimension(ctx.ctx)
        border = DrawPolyLine([(outline[0][0], outline[0][1]),
                          (outline[1][0], outline[0][1]),
                          (outline[1][0], outline[1][1]),
                          (outline[0][0], outline[1][1]),
                          (outline[0][0], outline[0][1])],
                          0.5, rgb(1, 0, 0, 1), 'solid')
        border.draw(ctx.ctx)
        factory.draw(ctx.ctx)


        
        if image_type == 'png':
            out = BytesIO()
            assert ctx.sfc, 'image cotext is not set.'
            ctx.sfc.write_to_png(out)
            #TODO write image when a filename is given 

    return out
