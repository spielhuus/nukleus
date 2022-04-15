from typing import List, Tuple
import math

from abc import ABC, abstractmethod

import gi
from pcbnew import ENDPOINT_START
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
import cairo
import numpy as np
from gi.repository import Pango, PangoCairo

from .model.rgb import rgb
from .model.SchemaElement import POS_T, PTS_T
from .model.Utils import f_coord
from .model.TextEffects import TextEffects, Justify

class BaseElement(ABC):
    pass

    @abstractmethod
    def dimension(self, _) -> PTS_T:
        pass

    @abstractmethod
    def draw(self, ctx):
        pass


class DrawLine(BaseElement):
    def __init__(self, pts: PTS_T, width: float, color: rgb, line_type: str) -> None:
        self.pts = pts
        self.width = width
        self.color = color
        self.line_type = line_type

    def dimension(self, _) -> PTS_T:
        return f_coord(np.array(self.pts))

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color.get())
        ctx.set_line_width(self.width)
        ctx.move_to(self.pts[0][0], self.pts[0][1])
        ctx.line_to(self.pts[1][0], self.pts[1][1])
        ctx.stroke_preserve()
        ctx.stroke()


class DrawPolyLine(BaseElement):
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


class DrawRect(BaseElement):
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


class DrawArc(BaseElement):
    def __init__(self, start: POS_T, mid: POS_T, end: POS_T, width: float, color: rgb, type: str, fill: rgb | None = None) -> None:
        point_a = np.array(start)
        point_b = np.array(mid)
        point_c = np.array(end)
        a = np.linalg.norm(point_c - point_b)  # type: ignore
        b = np.linalg.norm(point_c - point_a)  # type: ignore
        c = np.linalg.norm(point_b - point_a)  # type: ignore
        s = (a + b + c) / 2
        self.radius = a*b*c / 4 / np.sqrt(s * (s - a) * (s - b) * (s - c))
        b1 = a*a * (b*b + c*c - a*a)
        b2 = b*b * (a*a + c*c - b*b)
        b3 = c*c * (a*a + b*b - c*c)
        self.pos = np.column_stack((point_a, point_b, point_c)).dot(np.hstack((b1, b2, b3)))
        self.pos /= b1 + b2 + b3
        self.start_pos = start

        self.startAngle = (180/math.pi*math.atan2(start[1]-self.pos[1], start[0]-self.pos[0]))
        self.endAngle = (180/math.pi*math.atan2(end[1]-self.pos[1], end[0]-self.pos[0]))

        self.width = width
        self.color = color
        self.type = type
        self.fill = fill

    def dimension(self, _):
        return [(self.pos[0]-self.radius, self.pos[1]-self.radius),
                (self.pos[0]+self.radius, self.pos[1]+self.radius)]

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color.get())
        ctx.set_line_width(self.width)
        ctx.move_to(self.start_pos[0], self.start_pos[1])
        ctx.arc(self.pos[0], self.pos[1], self.radius,
                self.startAngle * (math.pi / 180),
                self.endAngle * (math.pi / 180))
        ctx.stroke()


class DrawCircle(BaseElement):
    """Draw a circle"""

    def __init__(self, pos: POS_T, radius: float, width: float, color: rgb,
                 type: str, fill: rgb | None = None) -> None:
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
        ctx.arc(self.pos[0], self.pos[1], self.radius, 0, 2*math.pi)
        ctx.stroke_preserve()
        if self.fill:
            ctx.set_source_rgba(*self.fill.get())
            ctx.fill()
        ctx.stroke()


class DrawElipse(BaseElement):
    """Draw a circle"""

    def __init__(self, pos: POS_T, radius1: float, radius2: float, width: float, color: rgb, type: str, fill: rgb | None = None) -> None:
        """
        Initialize a Circle object.

        :param pos POS_T: Center of the circle.
        :param radius1 float: Radius of the circle.
        :param radius2 float: Radius of the circle.
        :param width float: Line width.
        :param color rgb: Line color.
        :param type str: Line type.
        :param fill rgb|None: Fill color, default is no fill.
        """
        self.pos = pos
        self.radius1 = radius1
        self.radius2 = radius2
        self.width = width
        self.color = color
        self.type = type
        self.fill = fill

    def dimension(self, _):
        return f_coord(self.pos)

    def draw(self, ctx):
        ctx.save()
        radius = self.radius1
        if self.radius1 > self.radius2:
            ctx.scale(self.radius1/self.radius2, 1)
        else:
            radius = self.radius2
            ctx.scale(1, self.radius2/self.radius1)
        ctx.set_line_width(self.width)
        ctx.set_source_rgba(*self.color.get())
        ctx.arc(self.pos[0], self.pos[1], radius, 0, 100)
        ctx.stroke_preserve()
        #ctx.fill()
        ctx.stroke()
        ctx.restore()


class DrawText(BaseElement):
    """Draw a text to the context."""
    def __init__(self, pos: POS_T, text: str, rotation, text_effects: TextEffects) -> None:
        self.pos = pos
        self.text = text
        self.rotation = rotation if rotation < 180 else rotation-180
        self.font_face = text_effects.face
        self.font_width = text_effects.font_width
        self.font_height = text_effects.font_height
        self.font_weight = text_effects.font_style
        self.font_thickness = text_effects.font_thickness
        self.justify = text_effects.justify
        self.hidden = text_effects.hidden


    def dimension(self, ctx: cairo.Context) -> List[Tuple[float, float]]:
        layout = PangoCairo.create_layout(ctx)
        desc = Pango.FontDescription.from_string(f"{self.font_face} {self.font_width}")
        layout.set_font_description(desc)
        layout.set_text(self.text)

        size = layout.get_size()
        size_w = float(size[0]) / Pango.SCALE
        size_h = float(size[1]) / Pango.SCALE

        return [(self.pos[0], self.pos[1]), (self.pos[0]+size_w, self.pos[1]+size_h)]

    def draw(self, ctx):
        ctx.save()

        pos_x, pos_y = (self.pos[0], self.pos[1])
        dim = self.dimension(ctx)
        width = float(dim[1][0])
        height = float(dim[1][1])
        if self.rotation == 0:
            if Justify.LEFT in self.justify:
                pass
            elif Justify.RIGHT in self.justify:
                pos_x += (pos_x - width)
            else:
                pos_x += (pos_x - width) / 2

            if Justify.TOP in self.justify:
                pass
            elif Justify.BOTTOM in self.justify:
                pos_y += (pos_y - height)
            else:
                pos_y += (pos_y - height) / 2
        else:
            if Justify.LEFT in self.justify:
                pass
            elif Justify.RIGHT in self.justify:
                pos_y -= (pos_x - width)
            else:
                pos_y -= (pos_x - width) / 2

            if Justify.TOP in self.justify:
                pass
            elif Justify.BOTTOM in self.justify:
                pos_x += (pos_y - height)
            else:
                pos_x += (pos_y - height) / 2


        ctx.translate(pos_x, pos_y)
        ctx.set_source_rgba(*rgb(0, 0, 0, 1).get())

        layout = PangoCairo.create_layout(ctx)
        ctx.rotate((270 if self.rotation == 90 else self.rotation) * 3.14 / 180)

        desc = Pango.FontDescription.from_string(f"{self.font_face} {self.font_width}")
        layout.set_font_description(desc)

        layout.set_text(self.text)
        PangoCairo.show_layout(ctx, layout)

        ctx.stroke()
        ctx.restore()


class DrawDimension(BaseElement):
    """Draw a dimension to the context."""
    def __init__(self, pts: PTS_T, height: float, angle: float, leader: float, text: str,
                 width: float, color: rgb, text_effects: TextEffects) -> None:
        self.pts = pts
        self.height = height
        self.angle = angle
        self.leader = leader
        self.text = text
        self.width = width
        self.color = color
        self.text_effects = text_effects

    def dimension(self, ctx: cairo.Context) -> List[Tuple[float, float]]:
#        layout = PangoCairo.create_layout(ctx)
#        desc = Pango.FontDescription.from_string(f"{self.font_face} {self.font_width}")
#        layout.set_font_description(desc)
#        layout.set_text(self.text)
#
#        size = layout.get_size()
#        size_w = float(size[0]) / Pango.SCALE
#        size_h = float(size[1]) / Pango.SCALE
#
#        return [(self.pos[0], self.pos[1]), (self.pos[0]+size_w, self.pos[1]+size_h)]
        return  [0, 0]

    def draw(self, ctx):
        ctx.save()

        #calculate the dimension line ends
        v = np.array(self.pts[1]) - np.array(self.pts[0])
        dist =  np.array((-v[1], v[0])) / math.sqrt(v[0]**2 + v[1]**2) * self.height
        leader =  np.array((-v[1], v[0])) / math.sqrt(v[0]**2 + v[1]**2) * (self.height + self.leader)
        mid_x = self.pts[0][0] + (self.pts[1][0] - self.pts[0][0]) / 2;
        mid_y = self.pts[0][1] + (self.pts[1][1] - self.pts[0][1]) / 2;

        # Draw dimension line
        ctx.set_line_width(self.width)
        ctx.set_source_rgba(*self.color.get())

        ctx.move_to(self.pts[0][0], self.pts[0][1])
        ctx.line_to(self.pts[0][0] + leader[0], self.pts[0][1] + leader[1])

        ctx.move_to(self.pts[1][0], self.pts[1][1])
        ctx.line_to(self.pts[1][0] + leader[0], self.pts[1][1] + leader[1])

        ctx.move_to(self.pts[0][0] + dist[0], self.pts[0][1] + dist[1])
        ctx.line_to(self.pts[1][0] + dist[0], self.pts[1][1] + dist[1])

        ctx.arc(self.pts[0][0] + dist[0], self.pts[0][1] + dist[1], 0.3, 0, 2*math.pi)
        ctx.arc(self.pts[1][0] + dist[0], self.pts[1][1] + dist[1], 0.3, 0, 2*math.pi)

        # Draw dimension text
        #ctx.translate(*self.pts[1])
        #ctx.move_to(self.pts[0][0], self.pts[0][1] + leader[1])
        ctx.move_to(mid_x, mid_y + leader[1])
        ctx.set_source_rgba(*rgb(0, 0, 0, 1).get())

        layout = PangoCairo.create_layout(ctx)
        print(f'with: {self.pts[1][0] - self.pts[0][0]}')
        layout.set_width(self.pts[1][0] - self.pts[0][0])
        layout.set_height(self.leader)
        layout.set_alignment(Pango.Alignment.CENTER)

        #desc = Pango.FontDescription.from_string(f"{self.font_face} {self.font_width}")
        desc = Pango.FontDescription.from_string(f'osifont 2')
        layout.set_font_description(desc)

        layout.set_text(self.text)
        PangoCairo.show_layout(ctx, layout)

        ctx.stroke()
        ctx.restore()
