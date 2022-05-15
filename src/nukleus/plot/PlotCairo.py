from typing import IO

import math
import numpy as np

import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
import cairo
from gi.repository import Pango, PangoCairo

from nukleus.ModelBase import Justify, rgb
from nukleus.AbstractPlot import AbstractPlot
from ..Typing import *


class PlotCairo(AbstractPlot):
    def __init__(self, file: IO, width: float, height: float, dpi: int, scale: int = 1):
        self.file = file
        self.width = width
        self.height = height
        self.dpi = dpi
        self.scale = scale

        self.sfc = None
        if file.endswith('.pdf'):
            self.sfc = cairo.PDFSurface(
                file, width * scale, height * scale)
        else:
            self.sfc = cairo.SVGSurface(
                file, width * scale, height * scale)

        self.ctx = cairo.Context(self.sfc)
        self.ctx.scale(scale, scale)

    def polyline(self, pts: PTS_T, width: float, color: rgb, fill: rgb|None = None)-> None:
        self.ctx.set_source_rgba(*color.get())
        self.ctx.set_line_width(self.width)
        self.ctx.move_to(pts[0][0], pts[0][1])
        for point in pts[1:]:
            self.ctx.line_to(point[0], point[1])
        self.ctx.stroke_preserve()
        if fill:
            self.ctx.set_source_rgba(*fill.get())
            self.ctx.fill()
        self.ctx.stroke()

    def rectangle(self, start: POS_T, end: POS_T, width: float, color: rgb, fill: rgb|None=None) -> None:
        verts = [
            (start[0], start[1]),
            (start[0], end[1]),
            (end[0], end[1]),
            (end[0], start[1]),
            (start[0], start[1]),
        ]
        self.polyline(verts, width, color , fill)

    def line(self, pts: PTS_T, width: float, color: rgb) -> None:
        self.ctx.set_source_rgba(*color.get())
        self.ctx.set_line_width(width)
        self.ctx.move_to(pts[0][0], pts[0][1])
        self.ctx.line_to(pts[1][0], pts[1][1])
        self.ctx.stroke_preserve()
        self.ctx.stroke()

    def circle(self, pos: POS_T, radius: float, width: float, color: rgb, fill: rgb|None=None) -> None:
        self.ctx.set_line_width(width)
        self.ctx.set_source_rgba(*color.get())
        self.ctx.arc(pos[0], pos[1], radius, 0, 2*math.pi)
        self.ctx.stroke_preserve()
        if fill:
            self.ctx.set_source_rgba(*fill.get())
            self.ctx.fill()
        self.ctx.stroke()

    def arc(self, pos: POS_T, radius: float, start: float, end: float, width: float, color: rgb, fill: rgb|None=None) -> None:
        #self.startAngle = (180/math.pi*math.atan2(start[1]-self.pos[1], start[0]-self.pos[0]))
        #self.endAngle = (180/math.pi*math.atan2(end[1]-self.pos[1], end[0]-self.pos[0]))

        self.ctx.set_source_rgba(*color.get())
        self.ctx.set_line_width(self.width)
        self.ctx.move_to(pos[0], pos[1])
        self.ctx.arc(pos[0], pos[1], radius,
                0 * (math.pi / 180),
                360 * (math.pi / 180))
        self.ctx.stroke()

    def text(self, pos: POS_T, text: str, font_height: float, font_width: float,
            face: str, rotate: float, style: str, thickness: float,
            color: rgb, align: List[Justify]) -> None:

        self.ctx.save()

        pos_x, pos_y = (pos[0], pos[1])
#        dim = self.dimension(self.ctx.
#        width = float(dim[1][0])
#        height = float(dim[1][1])
#        if self.rotation == 0:
#            if Justify.LEFT in self.justify:
#                pass
#            elif Justify.RIGHT in self.justify:
#                pos_x += (pos_x - width)
#            else:
#                pos_x += (pos_x - width) / 2
#
#            if Justify.TOP in self.justify:
#                pass
#            elif Justify.BOTTOM in self.justify:
#                pos_y += (pos_y - height)
#            else:
#                pos_y += (pos_y - height) / 2
#        else:
#            if Justify.LEFT in self.justify:
#                pass
#            elif Justify.RIGHT in self.justify:
#                pos_y -= (pos_x - width)
#            else:
#                pos_y -= (pos_x - width) / 2
#
#            if Justify.TOP in self.justify:
#                pass
#            elif Justify.BOTTOM in self.justify:
#                pos_x += (pos_y - height)
#            else:
#                pos_x += (pos_y - height) / 2


        self.ctx.translate(pos_x, pos_y)
        self.ctx.set_source_rgba(*rgb(0, 0, 0, 1).get())

        layout = PangoCairo.create_layout(self.ctx)
        self.ctx.rotate((270 if rotate == 90 else rotate) * 3.14 / 180)

        desc = Pango.FontDescription.from_string(f"{face} {font_width}")
        layout.set_font_description(desc)

        layout.set_text(text)
        PangoCairo.show_layout(self.ctx, layout)

        self.ctx.stroke()
        self.ctx.restore()

    def end(self) -> None:
        self.ctx.fill()
        assert self.sfc, 'Image Surface not set.'
        self.sfc.finish()
        self.sfc.flush()
