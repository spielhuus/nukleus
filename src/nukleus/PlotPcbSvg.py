from abc import ABC, abstractmethod
from io import BytesIO
from typing import IO, Dict, List, Tuple, Type, cast
import math

import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')

import numpy as np
from gi.repository import Pango, PangoCairo

from .model.PcbGraphicItems import PcbLine
from .model.PcbSegment import PcbSegment
from .model.Footprint import Footprint

from .model.FootprintGraphicsItems import (FootprintArc, FootprintGraphicsItems,
                                                  FootprintLine, FootprintText, FootprintCircle, FootprintText, FootprintCircle)

from .model import (FillType, GlobalLabel, Junction, Justify, LibrarySymbol,
                    LocalLabel, NoConnect, Pin, StrokeDefinition, Symbol,
                    TextEffects, rgb)
from .model.GraphicalText import GraphicalText
from .model.GraphicItem import Arc, Circle, Polyline, Rectangle
from .model.HierarchicalSheetInstance import HierarchicalSheetInstance
from .model.SchemaElement import PTS_T, POS_T, SchemaElement
from .PCB import PCB
from .model.SymbolInstance import SymbolInstance
from .model.Utils import add, f_coord, isUnit, transform
from .model.Wire import Wire
from .PlotBase import (DrawArc, DrawCircle, DrawLine, DrawPolyLine, DrawRect,
                       DrawText, DrawElipse)
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


class NodeLine(Node):
    """Draw a Line"""

    def __init__(self, element: PcbLine, theme: str) -> None:
        self.line = DrawLine(
            [element.start, element.end],
            themes[theme]["no_connect"].width, # type: ignore
            themes[theme]["no_connect"].color, # type: ignore
            themes[theme]["no_connect"].stroke_type # type: ignore
        )

    def dimension(self, ctx) -> PTS_T:
        return self.line.dimension(ctx)

    def draw(self, ctx) -> None:
        return self.line.draw(ctx)


class NodeSegment(Node):
    """Draw a Segment"""

    def __init__(self, element: PcbSegment, theme: str) -> None:
        self.line = DrawLine(
            [element.start, element.end],
            element.width,
            themes[theme]["no_connect"].color, # type: ignore
            themes[theme]["no_connect"].stroke_type # type: ignore
        )

    def dimension(self, ctx) -> PTS_T:
        return self.line.dimension(ctx)

    def draw(self, ctx) -> None:
        return self.line.draw(ctx)


class NodeFootprint(Node):
    """Draw a Segment"""

    def __init__(self, element: Footprint, theme: str) -> None:
        self.line: List[Node] = []
        for graph in element.GRAPHIC_ITEMS:
            if isinstance(graph, FootprintLine):
                self.line.append(DrawLine(
                    transform(element, [graph.start, graph.end]),
                    graph.width,
                    themes[theme]["no_connect"].color, # type: ignore
                    themes[theme]["no_connect"].stroke_type # type: ignore
                ))
            elif isinstance(graph, FootprintText):
                if not graph.hide:
                    self.line.append(DrawText(
                        transform(element, graph.pos),
                        graph.text,
                        graph.angle,
                        graph.effects
                    ))
            elif isinstance(graph, FootprintCircle):
                x0 = graph.center[0]
                y0 = graph.center[1]
                x1 = graph.end[0]
                y1 = graph.end[1]
                radius = math.sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0))
                self.line.append(DrawCircle(
                    transform(element, graph.center),
                    radius,
                    graph.width,
                    rgb(1, 0, 0, 1),
                    'stroke'
                ))
            elif isinstance(graph, FootprintArc):
                self.line.append(DrawArc(
                    transform(element, graph.start),
                    transform(element, graph.mid),
                    transform(element, graph.end),
                    graph.width,
                    rgb(0, 1, 0, 1),
                    'stroke'
                ))
            else:
                print(f'unkown footprint graph element {graph}')

        for pad in element.pads:
            if pad.shape == 'circle':
                self.line.append(DrawCircle(
                    transform(element, pad.pos),
                    pad.size[0]/2,
                    0.1, #pad.width,
                    rgb(0, 0, 1, 1),
                    'stroke'
                ))
            elif pad.shape == 'rect':
                self.line.append(DrawRect(
                    transform(element, [
                        (pad.pos[0]-pad.size[0]/2, pad.pos[1]-pad.size[1]/2),
                        (pad.pos[0]+pad.size[0]/2, pad.pos[1]-pad.size[1]/2),
                        (pad.pos[0]+pad.size[0]/2, pad.pos[1]+pad.size[1]/2),
                        (pad.pos[0]-pad.size[0]/2, pad.pos[1]+pad.size[1]/2),
                        (pad.pos[0]-pad.size[0]/2, pad.pos[1]-pad.size[1]/2),
                    ]),
                    0.1, #pad.width,
                    rgb(1, 0, 1, 1),
                    'stroke'
                ))
            elif pad.shape == 'oval':
                self.line.append(DrawElipse(
                    transform(element, pad.pos),
                    pad.size[0]/2,
                    pad.size[1]/2,
                    0.1, #pad.width,
                    rgb(1, 0, 1, 1),
                    'stroke'
                ))
            else:
                print(f'unkown footprint pad shape {pad.shape}')

    def dimension(self, ctx) -> PTS_T:
        return [] #self.line.dimension(ctx)

    def draw(self, ctx) -> None:
        return [x.draw(ctx) for x in self.line]

class NodeWire(Node):
    """Draw a Wire"""

    def __init__(self, element: Wire, theme: str) -> None:
        self.line = DrawLine(
            element.pts,
            themes[theme]["no_connect"].width,
            themes[theme]["no_connect"].color,
            themes[theme]["no_connect"].stroke_type
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
            themes[theme]["no_connect"].width,
            themes[theme]["no_connect"].color,
            themes[theme]["no_connect"].stroke_type
        )

    def dimension(self, ctx) -> PTS_T:
        return self.circle.dimension(ctx)

    def draw(self, ctx) -> None:
        return self.circle.draw(ctx)


class NodeLocalLabel(Node):
    """Plot a LocalLabel."""

    def __init__(self, element: LocalLabel, theme: str) -> None:
        self.text_effects = _merge_text_effects(
            element.text_effects, themes[theme]['text_effects'])
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
                ((width + self.theme['global_label']['hspacing']) / 2)
        elif self.element.angle == 90:
            y_pos = self.element.pos[1] - \
                ((width + self.theme['global_label']['hspacing']) / 2)
            x_pos = self.element.pos[0] + \
                ((height + self.theme['global_label']['vspacing']) / 2)
        elif self.element.angle == 180:
            x_pos = self.element.pos[0] - \
                ((width + self.theme['global_label']['hspacing']) / 2)
        elif self.element.angle == 270:
            y_pos = self.element.pos[1] + \
                ((width + self.theme['global_label']['hspacing']) / 2)
            x_pos = self.element.pos[0] - \
                ((height + self.theme['global_label']['vspacing']) / 2)

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
            element.text_effects, themes[theme]['text_effects'])
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
        box = [
            (width + self.theme['global_label']['hspacing'],
                -height/2 - self.theme['global_label']['vspacing']),
            (.6, - height/2 - self.theme['global_label']['vspacing']),
            (0, 0),
            (.6, height/2 + self.theme['global_label']['vspacing']),
            (width + self.theme['global_label']['hspacing'],
                height/2 + self.theme['global_label']['vspacing']),
            (width + self.theme['global_label']['hspacing'], -
                height/2 - self.theme['global_label']['vspacing']),
        ]
        box = DrawPolyLine(transform(self.element, box),
                           self.theme['global_label']['border_width'],
                           self.theme['global_label']['border_color'],
                           self.theme['global_label']['border_style'],
                           self.theme['global_label']['fill_color'])
        box.draw(ctx)

        x_pos = self.element.pos[0]
        y_pos = self.element.pos[1]
        if self.element.angle == 0:
            x_pos = self.element.pos[0] + \
                ((width + self.theme['global_label']['hspacing']) / 2)
        elif self.element.angle == 90:
            y_pos = self.element.pos[1] - \
                ((width + self.theme['global_label']['hspacing']) / 2)
            x_pos = self.element.pos[0] + \
                ((height + self.theme['global_label']['vspacing']) / 2)
        elif self.element.angle == 180:
            x_pos = self.element.pos[0] - \
                ((width + self.theme['global_label']['hspacing']) / 2)
        elif self.element.angle == 270:
            y_pos = self.element.pos[1] + \
                ((width + self.theme['global_label']['hspacing']) / 2)
            x_pos = self.element.pos[0] - \
                ((height + self.theme['global_label']['vspacing']) / 2)

        self.text_effects.justify = []
        text = DrawText((x_pos, y_pos),
                        self.element.text, self.element.angle, self.text_effects)
        text.draw(ctx)


class NodeGraphicalText(Node):
    def __init__(self, element: GraphicalText, theme: str) -> None:
        """Plot a GraphicalText."""
        text_effects = _merge_text_effects(
            element.text_effects, themes[theme]['text_effects'])
        self.text = DrawText(element.pos, element.text, 0, text_effects)

    def dimension(self, ctx) -> PTS_T:
        return self.text.dimension(ctx)

    def draw(self, ctx) -> None:
        return self.text.draw(ctx)


class NodeNoConnect(Node):
    """Plot NoConnect element."""

    def __init__(self, element: NoConnect, theme: str) -> None:
        width = themes[theme]["no_connect"].width
        color = themes[theme]["no_connect"].color
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

    def dimension(self, ctx) -> List[float]:
        return []  # res

    def draw(self, ctx):
        [x.draw(ctx) for x in self.lines]


class NodeSymbol(Node):
    def __init__(self, element: Symbol, theme: str) -> None:
        self.symbol = element
        self.graphs = []
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
                        fill = themes[theme]["component_outline"].color
                    if isinstance(draw, Polyline):
                        self.graphs.append(DrawPolyLine(
                            transform(element, draw.points),
                            width=pin_theme.width,
                            color=pin_theme.color,
                            type=pin_theme.stroke_type,
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
                            transform(element, verts),
                            width=pin_theme.width,
                            color=pin_theme.color,
                            type=pin_theme.stroke_type,
                            fill=fill,
                        ))

                    elif isinstance(draw, Arc):
                        self.graphs.append(DrawArc(
                            cast(POS_T, transform(element, draw.start)),
                            draw.mid,
                            draw.end,
                            draw.stroke_definition.width,
                            # TODO draw.stroke_definition.color,
                            rgb(1, 0, 0, 1),
                            draw.stroke_definition.stroke_type
                        ))
                        #dp = np.array([draw.x, draw.y])
                        # pl.arc(dp, draw.r, draw.start * 0.1, draw.end * 0.1,
                        #       linewidth, edgecolor, facecolor)

                    elif isinstance(draw, Circle):
                        self.graphs.append(DrawCircle(
                            cast(POS_T, transform(element, draw.center)),
                            draw.radius,
                            draw.stroke_definition.width,
                            draw.stroke_definition.color,
                            draw.stroke_definition.stroke_type
                        ))
                        # TODO pl.circle(dp, draw.r, linewidth, edgecolor, facecolor)
                    else:
                        print(f"unknown graph type: {draw}")
#                #
#        self.pos = element.pos
                for pin in subsym.pins:
                    if pin.length:
                        pin_theme = themes[theme]["pin"]
                        pin_pos = transform(pin)
                        self.lines.append(DrawLine(
                            transform(element, pin_pos),
                            width=pin_theme.width,
                            color=pin_theme.color,
                            line_type=pin_theme.stroke_type,
                        ))

                    if (not sym.pin_numbers_hide
                            and not sym.extends == "power"):

#TODO                        pin_offset = np.array(((0, 0.1), (0.1, 0)))
#                        pin_offset[0] = -abs(pin_offset[0])
#                        pin_offset[1] = abs(pin_offset[1])

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

                        text_effects = themes[theme]['pin_number']
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

#                        name_position = transform(element,
#                                                  pin.calc_pos(pin.pos, sym.pin_names_offset)[1])
#                        pin_pos = transform(element, transform(pin))
#                        name_position = np.array(
#                            pin_pos[1]) + sym.pin_names_offset
                        text_effects = themes[theme]['pin_name']
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
                field.text_effects, themes[theme]['text_effects'])
            if element.angle + field.angle == 180:
                if Justify.LEFT in text_effects.justify:
                    text_effects.justify = [Justify.RIGHT]
                elif Justify.RIGHT in text_effects.justify:
                    text_effects.justify = [Justify.LEFT]

            self.texts.append(
                DrawText(field.pos, field.value, angle, text_effects))
#            self.graphs.append(DrawCircle(  # TODO remove
#                field.pos,
#                .2,
#                themes[theme]["no_connect"].width,
#                rgb(1, 0, 0, 1),
#                themes[theme]["no_connect"].stroke_type
#            ))

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
        border = float(border_theme['width'])
        self.lines = [
            DrawPolyLine([
                (border, border),
                (width-border, border),
                (width-border, height-border),
                (border, height-border),
                (border, border)
            ], border_theme['line'].width, border_theme['line'].color, border_theme['line'].stroke_type),
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
                (width-border-100, height-border-35), value, 0, border_theme[f'comment_{key}']))

    def dimension(self, _) -> List[float]:
        return []

    def draw(self, ctx):
        [x.draw(ctx) for x in self.lines]


class ElementFactory:
    """Get the Draw object by type."""

    def __init__(self, pcb: PCB, theme: str = "kicad2000"):
        self._creators: Dict[Type[SchemaElement], Type] = {
            PcbLine: NodeLine,
            PcbSegment: NodeSegment,
            Footprint: NodeFootprint,
            Wire: NodeWire,
            Junction: NodeJunction,
            LocalLabel: NodeLocalLabel,
            GlobalLabel: NodeGlobalLabel,
            NoConnect: NodeNoConnect,
            Symbol: NodeSymbol,
            GraphicalText: NodeGraphicalText
        }
        self.nodes = []
        for element in pcb.elements:
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
        [x.draw(ctx) for x in self.nodes]


SCALE = 72.0 / 25.4


class PlotContext:
    def __init__(self, buffer, width: int, height: int, scale: float, image_type: str):
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


def plot(pcb: PCB, out: IO = BytesIO(), border: bool = False, scale: float = SCALE, image_type='svg', theme: str = "kicad2000") -> IO:

    # get the image type if out is a filename
    if isinstance(out, str):
        image_type = out.split('.')[-1]
        if image_type not in ['png', 'svg', 'pdf']:
            raise FileTypeException(
                'file type not in (png, svg, pdf)', image_type)

    factory = ElementFactory(pcb)
    # just draw and get the size
    # TODO what is the best size for that
    with PlotContext(BytesIO(), 297, 210, scale, image_type) as outline_ctx:
        outline = factory.dimension(outline_ctx.ctx)
        width = outline[1][0] - outline[0][0] + 2*BORDER
        height = outline[1][1] - outline[0][1] + 2*BORDER
        if border:
            if pcb.paper != '':
                paper = pcb.paper
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
                factory.nodes.append(NodeBorder(pcb, width, height, theme))

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
