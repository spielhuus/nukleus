from abc import ABC, abstractmethod
from copy import deepcopy
from io import BytesIO
from typing import IO, Dict, List, Text, Tuple, Type, cast
import random
import string
import re

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
from .model.Utils import add, f_coord, isUnit, transform
from .model.Wire import Wire
from .PlotBase import (BaseElement, DrawArc, DrawCircle, DrawLine, DrawPolyLine,
                       DrawRect, DrawText)
from .Schema import Schema
from .Theme import themes


def check_notebook():
    try:
        __IPYTHON__  # type: ignore
        return True
    except NameError:
        return False


BORDER = 5
PAPER = {
    'A4': (297, 210),
    'A3': (420, 297)
}


class FileTypeException(Exception):
    """Exception is raised when a filetype is not supported."""


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


def _mergeStrokeDefinition(stroke_definition: StrokeDefinition,
                           theme_stroke_definition: StrokeDefinition) -> StrokeDefinition:
    if not stroke_definition:
        return theme_stroke_definition

    stroke = deepcopy(stroke_definition)

    if stroke_definition.width == 0:
        stroke.width = theme_stroke_definition.width
    if stroke_definition.stroke_type == '':
        stroke.stroke_type = theme_stroke_definition.stroke_type
    if stroke_definition.color == rgb(0, 0, 0, 0):
        stroke.color = theme_stroke_definition.color

    return stroke


class Node(ABC):
    """Abstract Class for the Nodes"""

    @abstractmethod
    def __init__(self, element: SchemaElement, theme: str) -> None:
        pass

    @abstractmethod
    def dimension(self, ctx) -> PTS_T:
        pass

    @abstractmethod
    def draw(self, _):
        pass


class NodeWire(Node):
    """Draw a Wire"""

    def __init__(self, element: Wire, theme: str) -> None:
        self.line = DrawLine(
            element.pts,
            themes[theme]["no_connect"].width,  # type: ignore
            themes[theme]["no_connect"].color,  # type: ignore
            themes[theme]["no_connect"].stroke_type  # type: ignore
        )

    def dimension(self, ctx) -> PTS_T:
        return self.line.dimension(ctx)

    def draw(self, ctx) -> None:
        return self.line.draw(ctx)


class NodeJunction(Node):
    def __init__(self, element: Junction, theme: str) -> None:
        self.circle = DrawCircle(
            element.pos,
            .2,
            themes[theme]["no_connect"].width,  # type: ignore
            themes[theme]["no_connect"].color,  # type: ignore
            themes[theme]["no_connect"].stroke_type  # type: ignore
        )

    def dimension(self, ctx) -> PTS_T:
        return self.circle.dimension(ctx)

    def draw(self, ctx) -> None:
        return self.circle.draw(ctx)


class NodeLocalLabel(Node):
    """Plot a LocalLabel."""

    def __init__(self, element: LocalLabel, theme: str) -> None:
        self.text_effects = _merge_text_effects(
            element.text_effects, cast(TextEffects, themes[theme]['text_effects']))
        self.element = element
        self.theme = themes[theme]

    def dimension(self, ctx) -> List[Tuple[float, float]]:
        text = DrawText((self.element.pos[0], self.element.pos[1]),
                        self.element.text, 0, self.text_effects)
        return text.dimension(ctx)

    def draw(self, ctx) -> None:
        text = DrawText((self.element.pos[0], self.element.pos[1]),
                        self.element.text, 0, self.text_effects)
        text_dim = text.dimension(ctx)
        width = text_dim[1][0] - text_dim[0][0]
        height = text_dim[1][1] - text_dim[0][1]

        x_pos = self.element.pos[0]
        y_pos = self.element.pos[1]
        if self.element.angle == 0:
            x_pos = self.element.pos[0] + \
                ((width + self.theme['global_label']
                 ['hspacing']) / 2)  # type: ignore
        elif self.element.angle == 90:
            y_pos = self.element.pos[1] - \
                ((width + self.theme['global_label']
                 ['hspacing']) / 2)  # type: ignore
            x_pos = self.element.pos[0] + \
                ((height + self.theme['global_label']
                 ['vspacing']) / 2)  # type: ignore
        elif self.element.angle == 180:
            x_pos = self.element.pos[0] - \
                ((width + self.theme['global_label']
                 ['hspacing']) / 2)  # type: ignore
        elif self.element.angle == 270:
            y_pos = self.element.pos[1] + \
                ((width + self.theme['global_label']
                 ['hspacing']) / 2)  # type: ignore
            x_pos = self.element.pos[0] - \
                ((height + self.theme['global_label']
                 ['vspacing']) / 2)  # type: ignore

        text = DrawText((x_pos, y_pos), self.element.text,
                        self.element.angle, self.text_effects)
        text.draw(ctx)


class NodeGlobalLabel(Node):
    """Plot a global Label"""

    def __init__(self, element: GlobalLabel, theme: str) -> None:
        """
        Create the GlobalLabel object.

        :param element GlobalLabel: GlobalLabel description.
        :param theme str: Theme name.
        """
        self.text_effects = _merge_text_effects(
            element.text_effects, themes[theme]['text_effects'])  # type: ignore
        self.element = element
        self.theme = themes[theme]

    def dimension(self, ctx) -> List[Tuple[float, float]]:
        """
        Get the dimension of this element.

        :param ctx cairo.Context: The cairo context.
        :rtype List[Tuple[float, float]]: absolute dimension.
        """
        text = DrawText((self.element.pos[0], self.element.pos[1]),
                        self.element.text, 0, self.text_effects)
        text_dim = text.dimension(ctx)
        width = text_dim[1][0] - text_dim[0][0]
        height = text_dim[1][1] - text_dim[0][1]
        box = [
            (width + 2, - height/2 - 1),
            (.4, - height/2 - 1),
            (0, 0),
            (.4, height/2 + 1),
            (width + 2, height/2 + 1),
            (width + 2, - height/2 - 1),
        ]
        return transform(self.element, box)

    def draw(self, ctx: cairo.Context) -> None:
        text = DrawText((self.element.pos[0], self.element.pos[1]),
                        self.element.text, 0, self.text_effects)
        text_dim = text.dimension(ctx)
        width = text_dim[1][0] - text_dim[0][0]
        height = text_dim[1][1] - text_dim[0][1]
        pts = [
            (width + self.theme['global_label']['hspacing'],  # type: ignore
                -height/2 - self.theme['global_label']['vspacing']),  # type: ignore
            (.6, - height/2 - self.theme['global_label']['vspacing']), # type: ignore
            (0, 0),
            (.6, height/2 + self.theme['global_label']
             ['vspacing']),  # type: ignore
            (width + self.theme['global_label']['hspacing'],  # type: ignore
                height/2 + self.theme['global_label']['vspacing']),  # type: ignore
            (width + self.theme['global_label']['hspacing'], -  # type: ignore
                height/2 - self.theme['global_label']['vspacing']),  # type: ignore
        ]
        box = DrawPolyLine(transform(self.element, pts),
                           self.theme['global_label']['border_width'], # type: ignore
                           self.theme['global_label']['border_color'], # type: ignore
                           self.theme['global_label']['border_style'], # type: ignore
                           self.theme['global_label']['fill_color'])  # type: ignore
        box.draw(ctx)

        x_pos = self.element.pos[0]
        y_pos = self.element.pos[1]
        if self.element.angle == 0:
            x_pos = self.element.pos[0] + \
                ((width + self.theme['global_label']
                 ['hspacing']) / 2)  # type: ignore
        elif self.element.angle == 90:
            y_pos = self.element.pos[1] - \
                ((width + self.theme['global_label']
                 ['hspacing']) / 2)  # type: ignore
            x_pos = self.element.pos[0] + \
                ((height + self.theme['global_label']
                 ['vspacing']) / 2)  # type: ignore
        elif self.element.angle == 180:
            x_pos = self.element.pos[0] - \
                ((width + self.theme['global_label']
                 ['hspacing']) / 2)  # type: ignore
        elif self.element.angle == 270:
            y_pos = self.element.pos[1] + \
                ((width + self.theme['global_label']
                 ['hspacing']) / 2)  # type: ignore
            x_pos = self.element.pos[0] - \
                ((height + self.theme['global_label']
                 ['vspacing']) / 2)  # type: ignore

        self.text_effects.justify = []
        text = DrawText((x_pos, y_pos),
                        self.element.text, self.element.angle, self.text_effects)
        text.draw(ctx)


class NodeGraphicalText(Node):
    def __init__(self, element: GraphicalText, theme: str) -> None:
        """Plot a GraphicalText."""
        text_effects = _merge_text_effects(
            element.text_effects, themes[theme]['text_effects'])   # type: ignore
        self.text = DrawText(element.pos, element.text, 0, text_effects)

    def dimension(self, ctx) -> PTS_T:
        return cast(PTS_T, self.text.dimension(ctx))

    def draw(self, ctx) -> None:
        return self.text.draw(ctx)


class NodeNoConnect(Node):
    """Plot NoConnect element."""

    def __init__(self, element: NoConnect, theme: str) -> None:
        width = themes[theme]["no_connect"].width  # type: ignore
        color = themes[theme]["no_connect"].color  # type: ignore
        type = themes[theme]["no_connect"].stroke_type
        o: float = 0.5
        self.lines = [
            DrawLine(
                cast(PTS_T, [add(element.pos, (o, -o)),
                             add(element.pos, (-o, o))]),
                width,
                color,
                type,
            ),
            DrawLine(
                cast(PTS_T, [add(element.pos, (o, -o)),
                             add(element.pos, (-o, o))]),
                width,
                color,
                type,
            ),
        ]

    def dimension(self, ctx) -> PTS_T:
        return cast(PTS_T, self.lines[0].dimension(ctx))

    def draw(self, ctx):
        for line in self.lines:
            line.draw(ctx)


class NodeSymbol(Node):
    def __init__(self, element: Symbol, theme: str) -> None:
        self.symbol: Symbol = element
        self.graphs: List[BaseElement] = []
        self.lines = []
        self.texts = []
        assert element.library_symbol, 'library symbol is not set'
        sym = element.library_symbol
        for subsym in sym.units:
            if isUnit(subsym, element.unit):
                for draw in subsym.graphics:
                    pin_theme = themes[theme]['component_outline']
#                        draw.stroke_definition,
#                        theme["component_outline"],
#                    )
                    fill = None
                    if draw.fill == FillType.BACKGROUND:
                        fill = themes[theme]["component_body"]
                    elif draw.fill == FillType.FOREGROUND:
                        fill = themes[theme]["component_outline"].color # type: ignore
                    if isinstance(draw, Polyline):
                        self.graphs.append(DrawPolyLine(
                            transform(element, draw.points),
                            width=pin_theme.width,  # type: ignore
                            color=pin_theme.color,  # type: ignore
                            type=pin_theme.stroke_type,  # type: ignore
                            fill=fill,  # type: ignore
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
                            transform(element, verts),
                            width=pin_theme.width,  # type: ignore
                            color=pin_theme.color,  # type: ignore
                            type=pin_theme.stroke_type,  # type: ignore
                            fill=fill,  # type: ignore
                        ))

                    elif isinstance(draw, Arc):
                        stroke = _mergeStrokeDefinition(
                            draw.stroke_definition,
                            themes[theme]['component_outline'])  # type: ignore
                        self.graphs.append(DrawArc(
                            cast(POS_T, transform(element, draw.start)),
                            cast(POS_T, transform(element, draw.mid)),
                            cast(POS_T, transform(element, draw.end)),
                            stroke.width,
                            stroke.color,
                            stroke.stroke_type
                        ))
                        #dp = np.array([draw.x, draw.y])
                        # pl.arc(dp, draw.r, draw.start * 0.1, draw.end * 0.1,
                        #       linewidth, edgecolor, facecolor)

                    elif isinstance(draw, Circle):
                        stroke = _mergeStrokeDefinition(
                            draw.stroke_definition,
                            themes[theme]['component_outline']) # type: ignore
                        self.graphs.append(DrawCircle(
                            cast(POS_T, transform(element, draw.center)),
                            draw.radius,
                            stroke.width,
                            stroke.color,
                            stroke.stroke_type
                        ))
                    else:
                        print(f"unknown graph type: {draw}")

                for pin in subsym.pins:
                    if pin.length:
                        pin_theme = themes[theme]["pin"]
                        pin_pos = transform(pin)
                        self.lines.append(DrawLine(
                            transform(element, pin_pos),
                            width=pin_theme.width,  # type: ignore
                            color=pin_theme.color,  # type: ignore
                            line_type=pin_theme.stroke_type,  # type: ignore
                        ))

                    if (not sym.pin_numbers_hide
                            and not sym.extends == "power"):

                        pin_pos = transform(element, transform(pin))
                        t_pos_x = pin_pos[0][0]
                        t_pos_y = pin_pos[0][1]

                        if pin.angle == 0:
                            t_pos_x += (pin_pos[1][0] - pin_pos[0][0]) / 2
                            t_pos_y -= 0.5
                        elif pin.angle == 90:
                            t_pos_y += (pin_pos[0][1] - pin_pos[1][1]) / 2
                            t_pos_x += 0.5
                        elif pin.angle == 180:
                            t_pos_x += (pin_pos[1][0] - pin_pos[0][0]) / 2
                            t_pos_y -= 0.5
                        elif pin.angle == 270:
                            t_pos_y += (pin_pos[1][1] - pin_pos[0][1]) / 2
                            t_pos_x += 0.5

                        text_effects: TextEffects = cast(
                            TextEffects, themes[theme]['pin_number'])
                        self.texts.append(
                            DrawText((t_pos_x, t_pos_y), pin.number[0], 0, text_effects))

                    if (pin.name[0] != "~"
                        and not pin.hidden
                            and not sym.extends == "power"):

                        pin_pos = transform(element, transform(pin))
                        t_pos_x = pin_pos[0][0]
                        t_pos_y = pin_pos[0][1]

                        if pin.angle == 0:
                            t_pos_x = pin_pos[1][0] + sym.pin_names_offset * 5
                        elif pin.angle == 90:
                            t_pos_y = pin_pos[1][1] + sym.pin_names_offset * 5
                        elif pin.angle == 180:
                            t_pos_x = pin_pos[0][0] - sym.pin_names_offset * 5
                        elif pin.angle == 270:
                            t_pos_y = pin_pos[0][1] - sym.pin_names_offset * 5

                        # type: ignore
                        text_effects = themes[theme]['pin_name'] # type: ignore
                        self.texts.append(
                            DrawText((t_pos_x, t_pos_y), pin.name[0], pin.angle, text_effects))

        # Add the visible text properties
        for field in element.properties:
            if field.text_effects and field.text_effects.hidden:
                continue
            if field.value == "~":
                continue

            angle = element.angle + field.angle
            if angle == 360:
                angle = 0
            if angle == 180:
                angle = 0

            text_effects = _merge_text_effects(
                field.text_effects, cast(TextEffects, themes[theme]['text_effects']))
            if element.angle + field.angle == 180:
                if Justify.LEFT in text_effects.justify:
                    text_effects.justify = [Justify.RIGHT]
                elif Justify.RIGHT in text_effects.justify:
                    text_effects.justify = [Justify.LEFT]

            self.texts.append(
                DrawText(field.pos, field.value, angle, text_effects))

    def dimension(self, ctx) -> PTS_T:
        if not self.symbol.on_schema:
            return []
        pts = []
        for graph in self.graphs:
            pts.append(graph.dimension(ctx))
        for line in self.lines:
            pts.append(line.dimension(ctx))
        for text in self.texts:
            pts.append(text.dimension(ctx))
        return f_coord(np.array(pts))

    def draw(self, ctx):
        if self.symbol.on_schema:
            [x.draw(ctx) for x in self.graphs]
            [x.draw(ctx) for x in self.lines]
            [x.draw(ctx) for x in self.texts]


class NodeBorder(Node):
    def __init__(self, schema: Schema, width: float, height: float, theme: str) -> None:
        #        text_effects = _merge_text_effects(
        #                element.text_effects, themes[theme]['text_effects'])
        border_theme = themes[theme]['border']
        border = float(border_theme['width'])  # type: ignore
        self.lines = [
            DrawPolyLine([
                (border, border),
                (width-border, border),
                (width-border, height-border),
                (border, height-border),
                (border, border)
            ], border_theme['line'].width,  # type: ignore
                border_theme['line'].color,  # type: ignore
                border_theme['line'].stroke_type),  # type: ignore
            DrawPolyLine([
                (width-border-110., height-border-40),
                (width-border, height-border-40),
                (width-border, height-border),
                (width-border-110, height-border),
                (width-border-110, height-border-40)
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].stroke_type),
            DrawPolyLine([
                (width-border-110., height-border-20),
                (width-border, height-border-20),
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].stroke_type),
            DrawPolyLine([
                (width-border-110., height-border-border),
                (width-border, height-border-border),
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].stroke_type),
            DrawPolyLine([
                (width-border-110., height-border-10),
                (width-border, height-border-10),
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].stroke_type),
            DrawPolyLine([
                (width-border-110., height-border-15),
                (width-border, height-border-15),
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].stroke_type)
        ]
        for key, value in schema.comment.items():
            self.lines.append(DrawText(
                (width-border-100, height-border-35), value, 0,
                border_theme[f'comment_{key}']))  # type: ignore

    def dimension(self, _) -> PTS_T:
        return []

    def draw(self, ctx):
        for line in self.lines:
            line.draw(ctx)


class ElementFactory:
    """Get the Draw object by type."""

    def __init__(self, schema: Schema, theme: str = "kicad2000"):
        self._creators: Dict[Type[SchemaElement], Type] = {
            Wire: NodeWire,
            Junction: NodeJunction,
            LocalLabel: NodeLocalLabel,
            GlobalLabel: NodeGlobalLabel,
            NoConnect: NodeNoConnect,
            Symbol: NodeSymbol,
            GraphicalText: NodeGraphicalText
        }
        self.nodes = []
        for element in schema.elements:
            creator = self._creators.get(type(element))
            if creator:
                self.nodes.append(creator(element, theme))  # type: ignore
            elif not isinstance(
                    element, (LibrarySymbol, SymbolInstance, HierarchicalSheetInstance)):
                print(f'element not found {type(element)}')

    def dimension(self, ctx) -> PTS_T:
        coords = []
        for node in self.nodes:
            node_coords = node.dimension(ctx)
            if len(node_coords) == 2:
                coords.append(node_coords)
        return f_coord(np.array(coords))

    def draw(self, ctx) -> None:
        for node in self.nodes:
            node.draw(ctx)


SCALE = 72.0 / 25.4


class PlotContext:
    def __init__(self, buffer, width: float, height: float, scale: float, image_type: str):
        self.sfc = None
        if image_type == 'pdf':
            self.sfc = cairo.PDFSurface(
                buffer, width * scale, height * scale)
        else:
            self.sfc = cairo.SVGSurface(
                buffer, width * scale, height * scale)

        self.ctx = cairo.Context(self.sfc)
        self.ctx.scale(scale, scale)
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

def _clean_svg(svg_string: str) -> str:
    rand = ''.join(random.choice(string.digits) for i in range(10))
    res = re.sub('id="glyph', f'id="glyph_{rand}_', svg_string)
    res = re.sub('href="#glyph', f'href="#glyph_{rand}_', res)
    return res

def plot(schema: Schema, out: IO|None = None, border: bool = False, scale: float = SCALE,
         image_type='svg', theme: str = "kicad2000") -> IO:

    # get the image type if out is a filename
    if not out:
        out = BytesIO()
    elif isinstance(out, str):
        image_type = out.split('.')[-1]
        if image_type not in ['png', 'svg', 'pdf']:
            raise FileTypeException(
                'file type not in (png, svg, pdf)', image_type)

    factory = ElementFactory(schema, theme=theme)
    # just draw and get the size
    # TODO what is the best size for that
    with PlotContext(BytesIO(), 297, 210, scale, image_type) as outline_ctx:
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

        # draw with the final size
        with PlotContext(out, width, height, scale, image_type) as ctx:
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
            svg_buffer = _clean_svg(str(out.read(), 'utf-8'))
            return SVG(data=svg_buffer)  # type: ignore
        except BaseException as err:
            print(f'can not display data {err}')

    return out
