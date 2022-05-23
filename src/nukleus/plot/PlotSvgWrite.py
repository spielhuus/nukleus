from typing import IO, Tuple

import numpy as np
import svgwrite
from svgwrite.container import SVG
from svgwrite.mixins import Transform
from svgwrite.utils import split_angle

from ..ModelBase import Justify, rgb

from ..AbstractPlot import AbstractPlot
from ..Typing import *
from ..transform import search_font


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

class PlotSvgWrite(AbstractPlot):
    def __init__(self, file: IO, width: float, height: float, dpi: int, scale: float = 3.543307):
        self.file = file
        self.width = width
        self.height = height
        self.dpi = dpi
        font = search_font('osifont')
        print(font)
        self.dwg = svgwrite.Drawing(filename=file, size=('297mm', '210mm'),
                                    profile="full", debug=True)
        self.dwg.embed_font('osifont', font)
        self.scale = scale

    def polyline(self, pts: PTS_T, width: float, color: rgb, fill: rgb|None = None)-> None:
        poly = self.dwg.polyline(
            pts, stroke=svgwrite.rgb(*_color(color)),
                fill='none' if fill is None else svgwrite.rgb(*_color(fill)), stroke_width=width)
        poly.scale(self.scale, self.scale)
        self.dwg.add(poly)

    def rectangle(self, start: POS_T, end: POS_T, width: float, color: rgb, fill: rgb|None=None) -> None:
        _start = start
        _end = end
        if start[0] > end[0]:
            _tmp = _start[0]
            _start = (_end[0], _start[1])
            _end = (_tmp, _end[1])
        if start[1] > end[1]:
            _tmp = _start[1]
            _start = (_start[0], _end[1])
            _end = (_end[0], _tmp)

        rect = self.dwg.rect(
            _start, np.array(_end) - np.array(_start), stroke=svgwrite.rgb(*_color(color)),
            fill='none' if fill is None else svgwrite.rgb(*_color(fill)),
            stroke_width=width)
        rect.scale(self.scale, self.scale)
        self.dwg.add(rect)

    def line(self, pts: PTS_T, width: float, color: rgb) -> None:
        line = self.dwg.line(
            pts[0], pts[1],
            stroke = svgwrite.rgb(*_color(color)), stroke_width=width)
        line.scale(self.scale, self.scale)
        self.dwg.add(line)

    def circle(self, pos: POS_T, radius: float, width: float, color: rgb, fill: rgb|None=None) -> None:
        line = self.dwg.circle(
            pos, radius,
            stroke = svgwrite.rgb(*_color(color)), stroke_width=width,
            fill='none' if fill is None else svgwrite.rgb(*_color(fill)))
        line.scale(self.scale, self.scale)
        self.dwg.add(line)

    def arc(self, pos: POS_T, radius: float, start: float, end: float, width: float, color: rgb, fill: rgb|None=None) -> None:
        line = self.dwg.circle(
            pos, radius,
            stroke = svgwrite.rgb(*_color(color)), stroke_width=width,
            fill='none' if fill is None else svgwrite.rgb(*_color(fill)))
        line.scale(self.scale, self.scale)
        self.dwg.add(line)

    def text(self, pos: POS_T, text: str, font_height: float, font_with: float,
            face: str, rotate: float, style: str, thickness: float,
            color: rgb, align: List[Justify]) -> None:

        line = self.dwg.text(
            text, pos,
            stroke=svgwrite.rgb(*_color(color)), stroke_width=thickness,
            font_size=font_height, font_family=face, #font_style=style,
            text_anchor=_align(align), alignment_baseline=_baseline(align),
            rotate=split_angle(rotate))
            #style = f"font-size:{font_height}; font-family:osifont monospace;")
        line.scale(self.scale, self.scale)
        #line.rotate(angle)
        self.dwg.add(line)

    def end(self) -> None:
        self.dwg.save()
