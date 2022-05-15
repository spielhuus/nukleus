from typing import IO, Tuple
import logging

from matplotlib.collections import LineCollection
from matplotlib.collections import EllipseCollection
from matplotlib.collections import PathCollection
from matplotlib.path import Path
import numpy as np
import math

from ..ModelBase import Justify, rgb

from ..AbstractPlot import AbstractPlot
from ..Typing import *

Y_TRANS = np.array([ 1, -1 ])

def _color(color: rgb) -> List[int]:
    cols = [int(c * 255) for c in color.get()[:-1]]
    #cols.append('%')
    return cols

def _align(align: List[Justify]):
    if Justify.LEFT in align:
        return 'start'
    if Justify.CENTER in align:
        return 'middle'
    return 'end'

def _baseline(align: List[Justify]):
    if Justify.TOP in align:
        return 'hanging'
    if Justify.BOTTOM in align:
        return 'baseline'
    return 'middle'

class PlotMatplotlib(AbstractPlot):
    def __init__(self, ax, width: float, height: float, dpi: int, scale: float = 3.543307):
        logging.debug("Create MatPlotlib plotter backend.")
        self.ax = ax
        self.width = width
        self.height = height
        self.dpi = dpi
        self.paths = []
        self.texts = []
        self.scale = scale
        self.pos = np.array([0.0, 0.0])

    def path(self, path, linewidth, edgecolor, facecolor):
        self.paths.append((path, linewidth, edgecolor, facecolor))

    def polyline(self, pts: PTS_T, width: float, color: rgb, fill: rgb|None = None)-> None:
        self.paths.append((Path(pts), width, color.get(), (0, 0, 0, 1) if fill is None else fill.get()))
#        poly = self.dwg.polyline(
#            pts, stroke=svgwrite.rgb(*_color(color)),
#                fill='none' if fill is None else svgwrite.rgb(*_color(fill)), stroke_width=width)
#        poly.scale(self.scale, self.scale)
#        self.dwg.add(poly)
#
    def rectangle(self, start: POS_T, end: POS_T, width: float, color: rgb, fill: rgb|None=None) -> None:
        pass

#        rect = self.dwg.rect(
#            start, np.array(end) - np.array(start), stroke=svgwrite.rgb(*_color(color)),
#            fill='none' if fill is None else svgwrite.rgb(*_color(fill)),
#            stroke_width=width)
#        rect.scale(self.scale, self.scale)
#        self.dwg.add(rect)

    def line(self, pts: PTS_T, width: float, color: rgb) -> None:
        self.paths.append((Path(pts), width, color.get(), (0, 0, 0, 1)))
#        line = self.dwg.line(
#            pts[0], pts[1],
#            stroke = svgwrite.rgb(*_color(color)), stroke_width=width)
#        line.scale(self.scale, self.scale)
#        self.dwg.add(line)

    def circle(self, pos: POS_T, radius: float, width: float, color: rgb, fill: rgb|None=None) -> None:
        pass
        #path = Path.circle(pos, radius)
        #self.path(path, width, color.get(), (0, 0, 0, 1) if not fill else fill.get())
#
#        line = self.dwg.circle(
#            pos, radius,
#            stroke = svgwrite.rgb(*_color(color)), stroke_width=width,
#            fill='none' if fill is None else svgwrite.rgb(*_color(fill)))
#        line.scale(self.scale, self.scale)
#        self.dwg.add(line)

    def arc(self, pos: POS_T, radius: float, start: float, end: float, width: float, color: rgb, fill: rgb|None=None) -> None:
        pass
        #path = Path.circle(pos, radius)
        #self.path(path, width, color.get(), fill)

#        line = self.dwg.circle(
#            pos, radius,
#            stroke = svgwrite.rgb(*_color(color)), stroke_width=width,
#            fill='none' if fill is None else svgwrite.rgb(*_color(fill)))
#        line.scale(self.scale, self.scale)
#        self.dwg.add(line)
#
    def text(self, pos: POS_T, text: str, font_height: float, font_with: float,
            face: str, rotate: float, style: str, thickness: float,
            color: rgb, align: List[Justify]) -> None:

        self.texts.append((pos, style, text, font_height, Justify.halign(align), Justify.valign(align), color.get()))

#        line = self.dwg.text(
#            text, pos,
#            stroke=svgwrite.rgb(*_color(color)), stroke_width=thickness,
#            font_size=font_height, font_family=face, #font_style=style,
#            text_anchor=_align(align), alignment_baseline=_baseline(align),
#            rotate=split_angle(rotate))
#        line.scale(self.scale, self.scale)
#        #line.rotate(angle)
#        self.dwg.add(line)

    def end(self) -> None:
        #trans = np.reshape(orientation, (2,2)).T

        for offset, normal, text, size, halign, valign, color in self.texts:
            #normal = np.matmul(normal, trans)
            #angle = math.atan2(-normal[1], normal[0]) * 180 / math.pi
            x, y = ((self.pos + offset) * Y_TRANS)

#            if angle >= 180 or angle < 0:
#                if halign == 'right':
#                    halign = 'left'
#                elif halign == 'left':
#                    halign = 'right'
#                if valign == 'top':
#                    valign = 'bottom'
#                elif valign == 'bottom':
#                    valign = 'top'
#                angle -= 180

            kw = { 'x': x,
                   'y': y,
                   'color': color,
                   #                               'font': 'sans-serif',
                   'fontsize': size,
                   's': text,
                   'rotation': 0, #angle,
                   'rotation_mode': 'anchor',
                   'horizontalalignment': halign,
                   'verticalalignment': valign,
                   'clip_on': True,
                   }

            self.ax.text(**kw)

        if self.paths:
            d = {}
            d['paths'] = []
            d['linewidths'] = []
            d['edgecolors'] = []
            d['facecolors'] = []

            for path, linewidth, edgecolor, facecolor in self.paths:
                verts = path.vertices
                #verts = np.matmul(verts, trans)
                verts = (self.pos + verts) * Y_TRANS
                path.vertices = verts

                d['paths'].append(path)
                d['linewidths'].append(linewidth)
                d['edgecolors'].append(edgecolor)
                d['facecolors'].append(facecolor)

            #pc = PathCollection(offset_position = 'data', **d)

            pc = PathCollection(**d)
            self.ax.add_collection(pc)

        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.axis('equal')
        #fig = self.ax.get_figure()
