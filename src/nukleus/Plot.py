from io import BytesIO
from typing import IO, List, Text

import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
import cairo
import numpy as np
from gi.repository import Pango, PangoCairo

from .model import (FillType, GlobalLabel, Junction, Justify, LibrarySymbol,
                    LocalLabel, NoConnect, Pin, StrokeDefinition, Symbol,
                    TextEffects, rgb)
from .model.GraphicalText import GraphicalText
from .model.GraphicItem import Arc, Circle, Polyline, Rectangle
from .model.HierarchicalSheetInstance import HierarchicalSheetInstance
from .model.SchemaElement import POS_T, PTS_T, SchemaElement
from .model.SymbolInstance import SymbolInstance
from .model.Wire import Wire
from .Schema import Schema
from .Theme import themes


def check_notebook():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


BORDER = 5
PAPER = {
    'A4': (297, 210),
    'A3': (420, 297)
}


def f_coord(arr): return [(np.min(arr[..., 0]), np.min(arr[..., 1])),
                          (np.max(arr[..., 0]), np.max(arr[..., 1]))]


class FileTypeException(Exception):
    pass


def _merge_text_effects(text_effects: TextEffects, theme_effects: TextEffects) -> TextEffects:
    if not text_effects:
        return theme_effects

    if text_effects.face == '':
        text_effects.face = theme_effects.face
    if text_effects.font_height == 0:
        text_effects.font_height = theme_effects.font_height
    if text_effects.font_width == 0:
        text_effects.font_width = theme_effects.font_width
    if text_effects.font_style == '':
        text_effects.font_style = theme_effects.font_style
    if text_effects.font_thickness == '':
        text_effects.font_thickness = theme_effects.font_thickness
    if len(text_effects.justify) == 0:
        text_effects.justify = theme_effects.justify

    return text_effects


class DrawLine:
    def __init__(self, pts: PTS_T, width: float, color: rgb, line_type: str) -> None:
        self.pts = pts
        self.width = width
        self.color = color
        self.line_type = line_type

    def dimension(self, _):
        return f_coord(np.array(self.pts))

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color.get())
        ctx.set_line_width(self.width)
        ctx.move_to(self.pts[0][0], self.pts[0][1])
        ctx.line_to(self.pts[1][0], self.pts[1][1])
        ctx.stroke_preserve()
        ctx.stroke()


class DrawPolyLine:
    """Draw a polyline"""

    def __init__(self, pts: PTS_T, width: float, color: rgb, type: str, fill: rgb | None = None) -> None:
        """
        Initialize the polyline object.

        :param pts PTS_T: Polyline points.
        :param width float: Line width.
        :param color rgb: Line color.
        :param type str: Line type.
        :param fill rgb|None: Fill the polyline. Default is no fill.
        """
        self.pts = pts
        self.width = width
        self.color = color
        self.type = type
        self.fill = fill

    def dimension(self, _):
        return f_coord(np.array(self.pts))

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color.get())
        ctx.set_line_width(self.width)
        ctx.move_to(self.pts[0][0], self.pts[0][1])
        for point in self.pts[1:]:
            ctx.line_to(point[0], point[1])
        ctx.stroke_preserve()
        if self.fill:
            ctx.set_source_rgba(*self.fill.get())
            ctx.fill()
        ctx.stroke()


class DrawRect:
    def __init__(self, pts: PTS_T, width: float, color: rgb, type: str, fill: rgb | None = None) -> None:
        self.pts = pts
        self.width = width
        self.color = color
        self.type = type
        self.fill = fill

    def dimension(self, _):
        return f_coord(np.array(self.pts))

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color.get())
        ctx.set_line_width(self.width)
        ctx.move_to(self.pts[0][0], self.pts[0][1])
        for point in self.pts[1:]:
            ctx.line_to(point[0], point[1])
        ctx.stroke_preserve()
        if self.fill:
            ctx.set_source_rgba(*self.fill.get())
            ctx.fill()
        ctx.stroke()


class DrawArc:
    def __init__(self, start: POS_T, mid: POS_T, end: POS_T, width: float, color: rgb, type: str, fill: rgb | None = None) -> None:
        self.start = start
        self.med = mid
        self.end = end
        self.width = width
        self.color = color
        self.type = type
        self.fill = fill

    def dimension(self, _):
        return f_coord(np.array(self.start))

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color.get())
        ctx.set_line_width(self.width)
        ctx.move_to(self.start[0], self.start[1])
        ctx.arc(self.start[0], self.start[1], self.med[0], 0, 100)
        ctx.stroke_preserve()
        if self.fill:
            ctx.set_source_rgba(*self.fill.get())
            ctx.fill()
        ctx.stroke()


class DrawCircle:
    """Draw a circle"""

    def __init__(self, pos: POS_T, radius: float, width: float, color: rgb, type: str, fill: rgb | None = None) -> None:
        """
        Initialize a Circle object.

        :param pos POS_T: Center of the circle.
        :param radius float: Radius of the circle.
        :param width float: Line width. 
        :param color rgb: Line color.
        :param type str: Line type.
        :param fill rgb|None: Fill color, default is no fill.
        """
        self.pos = pos
        self.radius = radius
        self.width = width
        self.color = color
        self.type = type
        self.fill = fill

    def dimension(self, _):
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
    def __init__(self, pos: POS_T, text: str, rotation, text_effects: TextEffects) -> None:
        self.pos = pos
        self.text = text
        self.rotation = rotation
        self.font_face = text_effects.face
        self.font_width = text_effects.font_width
        self.font_height = text_effects.font_height
        self.font_weight = text_effects.font_style
        self.font_thickness = text_effects.font_thickness
        self.justify = text_effects.justify
        self.hidden = text_effects.hidden

    def dimension(self, ctx):
        layout = PangoCairo.create_layout(ctx)
        pctx = layout.get_context()
        desc = Pango.FontDescription()
        desc.set_size(self.font_height*Pango.SCALE)
        desc.set_family(self.font_face)
        layout.set_font_description(desc)
        layout.set_alignment(Pango.Alignment.CENTER)
        font_options = cairo.FontOptions()
        font_options.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        PangoCairo.context_set_font_options(pctx, font_options)
        layout.set_text(self.text)
        size = layout.get_size()
        size_w = float(size[0]) / Pango.SCALE
        size_h = float(size[1]) / Pango.SCALE

        return [(self.pos[0], self.pos[1]), (self.pos[0]+size_w, self.pos[1]+size_h)]

    def draw(self, ctx):
        ctx.save()

        pos_x, pos_y = (self.pos[0], self.pos[1])
        width = float(self.dimension(ctx)[1][0])
        if Justify.LEFT in self.justify:
            pass
        elif Justify.RIGHT in self.justify:
            pos_x += (pos_x - width)
        else:
            pos_x += (pos_x - width) / 2

        height = float(self.dimension(ctx)[1][1])
        if Justify.TOP in self.justify:
            pass
        elif Justify.BOTTOM in self.justify:
            pos_y += (pos_y - height)
        else:
            pos_y += (pos_y - height) / 2

        #            x_bearing, y_bearing, width, height, x_advance, y_advance = \
        #                self.ctx.text_extents(string)
        #            x = x - (width + x_bearing)
        #            #y = y - (height + y_bearing)
        #        if Justify.TOP in text_effects.justify:
        #            x_bearing, y_bearing, width, height, x_advance, y_advance = \
        #                self.ctx.text_extents(string)
        #            #x = x - (width / 2 + x_bearing)
        #            y = y - (height + y_bearing)

        ctx.translate(pos_x, pos_y)
        layout = PangoCairo.create_layout(ctx)
        pctx = layout.get_context()
        # layout.set_width(pango.units_from_double(10))
        desc = Pango.FontDescription()
        desc.set_size(self.font_height*1024)
        desc.set_family(self.font_face)
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
        size = layout.get_size()
        size_w = float(size[0]) / Pango.SCALE
        size_h = float(size[1]) / Pango.SCALE
        size = (size_w, size_h)
        ctx.set_source_rgba(*rgb(.2, .2, .2, 1).get())
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
        text_effects = _merge_text_effects(
            element.text_effects, themes[theme]['text_effects'])
        self.text = DrawText(element.pos, element.text, 0, text_effects)

    def dimension(self, ctx) -> List[float]:
        return self.text.dimension(ctx)

    def draw(self, ctx) -> None:
        return self.text.draw(ctx)


class NodeGlobalLabel(Node):
    def __init__(self, element: GlobalLabel, theme: str) -> None:
        text_effects = _merge_text_effects(
            element.text_effects, themes[theme]['text_effects'])
        self.text = DrawText(element.pos, element.text, 0, text_effects)

    def dimension(self, ctx) -> List[float]:
        return self.text.dimension(ctx)

    def draw(self, ctx) -> None:
        return self.text.draw(ctx)


class NodeGraphicalText(Node):
    def __init__(self, element: GraphicalText, theme: str) -> None:
        text_effects = _merge_text_effects(
            element.text_effects, themes[theme]['text_effects'])
        self.text = DrawText(element.pos, element.text, 0, text_effects)

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
                (element.pos + np.array([o, -o]),
                 element.pos + np.array([-o, o])),
                width,
                color,
                type,
            ),
            DrawLine(
                (element.pos + np.array([o, -o]),
                 element.pos + np.array([-o, o])),
                width,
                color,
                type,
            ),
        ]

    def dimension(self, ctx) -> List[float]:
        return []  # res

    def draw(self, ctx):
        [x.draw(ctx) for x in self.lines]


class NodeSymbol(Node):
    def __init__(self, element: Symbol, theme: str) -> None:
        self.graphs = []
        self.lines = []
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

                    elif isinstance(draw, Arc):
                        self.graphs.append(DrawArc(
                            element._pos(draw.start),
                            draw.mid,
                            draw.end,
                            draw.stroke_definition.width,
                            # TODO draw.stroke_definition.color,
                            rgb(1, 0, 0, 1),
                            draw.stroke_definition.type
                        ))
                        #dp = np.array([draw.x, draw.y])
                        # pl.arc(dp, draw.r, draw.start * 0.1, draw.end * 0.1,
                        #       linewidth, edgecolor, facecolor)

                    elif isinstance(draw, Circle):
                        self.graphs.append(DrawCircle(
                            element._pos(draw.center),
                            draw.radius,
                            draw.stroke_definition.width,
                            # TODO draw.stroke_definition.color,
                            rgb(1, 0, 0, 1),
                            draw.stroke_definition.type
                        ))
                        # TODO pl.circle(dp, draw.r, linewidth, edgecolor, facecolor)
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
                            line_type=sd.type,
                        ))

                    if (
                        not sym.pin_numbers_hide
                        and not sym.extends == "power"
                    ):

                        o = np.array(((0, 0.1), (0.1, 0)))
                        o[0] = -abs(o[0])
                        o[1] = abs(o[1])

                        pp = element._pos(pin._pos())
                        text_effects = themes[theme]['pin_number']
                        self.texts.append(
                            DrawText(element.pos, pin.number[0], 0, text_effects))

                    if (
                        pin.name[0] != "~"
                        and not pin.hidden
                        and not sym.extends == "power"
                    ):

                        name_position = element._pos(
                            pin.calc_pos(pin.pos, sym.pin_names_offset)[1])
                        pp = element._pos(pin._pos())
                        _name_position = pp[1] + sym.pin_names_offset
                        text_effects = themes[theme]['pin_name']
                        self.texts.append(
                            DrawText(name_position, pin.name[0], 0, text_effects))

        # Add the visible text properties
        for field in element.properties:
            if field.text_effects and field.text_effects.hidden:
                continue
            if field.value == "~":
                continue

            angle = field.angle
#            angle = element.angle - field.angle
#            print(
#                f"FIELD ANGLE: {field.value} {field.angle} {element.angle} {angle}"
#            )
#            if angle >= 180:
#                angle -= 180
#            elif angle == 90:
#                angle = 270

            text_effects = _merge_text_effects(
                field.text_effects, themes[theme]['text_effects'])
            if element.angle + field.angle == 180:
                if Justify.LEFT in text_effects.justify:
                    text_effects.justify = [Justify.RIGHT]
                elif Justify.RIGHT in text_effects.justify:
                    text_effects.justify = [Justify.LEFT]

            self.texts.append(
                DrawText(field.pos, field.value, angle, text_effects))
            self.graphs.append(DrawCircle(
                field.pos,
                .2,
                themes[theme]["no_connect"].width,
                rgb(1, 0, 0, 1),
                themes[theme]["no_connect"].type
            ))

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


class NodeBorder(Node):
    def __init__(self, schema: Schema, width: float, height: float, theme: str) -> None:
        #        text_effects = _merge_text_effects(
        #                element.text_effects, themes[theme]['text_effects'])
        border_theme = themes[theme]['border']
        border = float(border_theme['width'])
        self.lines = [
            DrawPolyLine([
                (border, border),
                (width-border, border),
                (width-border, height-border),
                (border, height-border),
                (border, border)
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].type),
            DrawPolyLine([
                (width-border-110., height-border-40),
                (width-border, height-border-40),
                (width-border, height-border),
                (width-border-110, height-border),
                (width-border-110, height-border-40)
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].type),
            DrawPolyLine([
                (width-border-110., height-border-20),
                (width-border, height-border-20),
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].type),
            DrawPolyLine([
                (width-border-110., height-border-border),
                (width-border, height-border-border),
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].type),
            DrawPolyLine([
                (width-border-110., height-border-10),
                (width-border, height-border-10),
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].type),
            DrawPolyLine([
                (width-border-110., height-border-15),
                (width-border, height-border-15),
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].type),
            DrawText(
                (width-border-100, height-border-35), schema.comment_1, 0, border_theme['comment_1']),
            DrawText(
                (width-border-100, height-border-32), schema.comment_2, 0, border_theme['comment_2']),
            DrawText(
                (width-border-100, height-border-29), schema.comment_3, 0, border_theme['comment_3']),
            DrawText(
                (width-border-100, height-border-27), schema.comment_4, 0, border_theme['comment_4']),
        ]

    def dimension(self, _) -> List[float]:
        return []

    def draw(self, ctx):
        [x.draw(ctx) for x in self.lines]


class ElementFactory:
    def __init__(self, schema: Schema, theme: str = "kicad2000"):
        self._creators = {Wire: NodeWire, Junction: NodeJunction, LocalLabel: NodeLocalLabel,
                          GlobalLabel: NodeGlobalLabel, NoConnect: NodeNoConnect,
                          Symbol: NodeSymbol,
                          GraphicalText: NodeGraphicalText}
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
            self.sfc = cairo.PDFSurface(
                buffer, width / 25.4 * 72, height / 25.4 * 72)
        else:
            self.sfc = cairo.SVGSurface(
                buffer, width / 25.4 * 72, height / 25.4 * 72)

        self.ctx = cairo.Context(self.sfc)
        self.ctx.scale(72. / 25.4, 72. / 25.4)
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


def plot(schema: Schema, out: IO = BytesIO(), border: bool = False, image_type='svg', theme: str = "kicad2000") -> IO:

    # get the image type if out is a filename
    if isinstance(out, str):
        image_type = out.split('.')[-1]
        if image_type not in ['png', 'svg', 'pdf']:
            raise FileTypeException(
                'file type not in (png, svg, pdf)', image_type)

    factory = ElementFactory(schema)
    with PlotContext(BytesIO(), 297, 210, image_type) as outline_ctx:
        outline = factory.dimension(outline_ctx.ctx)
        width = outline[1][0] - outline[0][0] + 2*BORDER
        height = outline[1][1] - outline[0][1] + 2*BORDER
        if border:
            if schema.paper != '':
                paper = schema.paper
                width = PAPER[paper][0]
                height = PAPER[paper][1]
            else:
                raise ValueError(
                    'Border is set to true, but no paper size given')

        with PlotContext(out, width, height, image_type) as ctx:
            if not border:
                ctx.ctx.translate(-outline[0][0]+BORDER, -outline[0][1]+BORDER)
            else:
                factory.nodes.append(NodeBorder(schema, width, height, theme))
            factory.draw(ctx.ctx)

            if image_type == 'png':
                out = BytesIO()
                assert ctx.sfc, 'image cotext is not set.'
                ctx.sfc.write_to_png(out)

    if check_notebook():
        try:
            from IPython.display import SVG
            out.flush()
            out.seek(0)
            return SVG(data=out.getbuffer())
        except BaseException as err:
            print(f'can not display data {err}')

    return out
