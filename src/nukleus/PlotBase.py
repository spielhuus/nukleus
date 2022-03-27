from typing import List, Tuple

import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
import cairo
import numpy as np
from gi.repository import Pango, PangoCairo

from .model.rgb import rgb
from .model.SchemaElement import POS_T, PTS_T
from .model.Utils import f_coord
from .model.TextEffects import TextEffects, Justify

class DrawLine:
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
        assert self.rotation in (0, 90), f'self.rotation is {self.rotation}'
        ctx.save()

#        # TODO Draw pos circle
#        ctx.set_line_width(0.1)
#        ctx.set_source_rgba(*rgb(1, 0, 0, 1).get())
#        ctx.arc(self.pos[0], self.pos[1], .1, 0, 100)
#        ctx.stroke_preserve()
#        ctx.fill()
#        ctx.stroke()

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
        pctx = layout.get_context()
        ctx.rotate((270 if self.rotation == 90 else self.rotation) * 3.14 / 180)

        # layout.set_width(pango.units_from_double(10))
        desc = Pango.FontDescription()
        desc.set_size(self.font_height*1024)
        desc.set_family("Sans") #self.font_face)
        layout.set_font_description(desc)
        layout.set_alignment(Pango.Alignment.CENTER)
        fo = cairo.FontOptions()
        fo.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        PangoCairo.context_set_font_options(pctx, fo)


        layout.set_text(self.text)
        PangoCairo.show_layout(ctx, layout)

        # TODO remove draw box around text
#        size = layout.get_size()
#        size_w = float(size[0]) / Pango.SCALE
#        size_h = float(size[1]) / Pango.SCALE
#        size = (size_w, size_h)
#        ctx.set_source_rgba(*rgb(.2, .2, .2, 1).get())
#        ctx.set_line_width(0.1)
#        ctx.move_to(0, 0)
#        ctx.line_to(size[0], 0)
#        ctx.line_to(size[0], size[1])
#        ctx.line_to(0, size[1])
#        ctx.line_to(0, 0)
#        ctx.stroke_preserve()

        ctx.stroke()
        ctx.restore()