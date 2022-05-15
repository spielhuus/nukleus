from typing import IO, Tuple

import cv2 as cv
import numpy as np

from ..ModelBase import Justify, rgb

from ..AbstractPlot import AbstractPlot
from ..Typing import *


def _pos(pos: POS_T) -> Tuple[int, int]:
    return (int(pos[0]*10), int(pos[1]*10))

def _pts(pts: PTS_T):
    res = []
    for pos in pts:
        res.append((int(pos[0]*10), int(pos[1]*10)))
    return np.array([res], np.int32)

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

class PlotOpenCV(AbstractPlot):
    def __init__(self, file: IO, width: float, height: float, dpi: int, scale: float = 3.543307):
        self.file = file
        self.width = width
        self.height = height
        self.dpi = dpi
        self.scale = scale
        size = int(width*10), int(height*10), 3
        self._image = np.zeros(size, dtype=np.uint8)

    def polyline(self, pts: PTS_T, width: float, color: rgb, fill: rgb|None = None)-> None:
        line_type = 8
        cv.fillPoly(self._image, _pts(pts), (255, 255, 255), line_type)

    def rectangle(self, start: POS_T, end: POS_T, width: float, color: rgb, fill: rgb|None=None) -> None:
        _start = start
        _end = end
        if start[0] > end[0]:
            _tmp = _start[0]
            _start = (_end[0], _start[1])
            _end = (_tmp, _end[1])
        if start[1] > end[1]:
            _tmp = _start[1]
            _start = (start[0], _end[1])
            _end = (end[0], _tmp)

        line_type = 8
        cv.rectangle(self._image, _pos(_start), _pos(_end),
              (0, 255, 255),
              -1,
              8)

    def line(self, pts: PTS_T, width: float, color: rgb) -> None:
        line_type = 8
        cv.line(self._image, _pos(pts[0]), _pos(pts[1]), (0, 0, 0),
             int(width*10),
             line_type)

    def circle(self, pos: POS_T, radius: float, width: float, color: rgb, fill: rgb|None=None) -> None:
        line_type = 8
        cv.circle(self._image,
               _pos(pos),
               int(radius),
               (0, 0, 255),
               int(width*10),
               line_type)

    def arc(self, pos: POS_T, radius: float, start: float, end: float, width: float, color: rgb, fill: rgb|None=None) -> None:
        line_type = 8
        cv.circle(self._image,
               _pos(pos),
               radius,
               (0, 0, 255),
               int(width*10),
               line_type)

    def text(self, pos: POS_T, text: str, font_height: float, font_with: float,
            face: str, rotate: float, style: str, thickness: float,
            color: rgb, align: List[Justify]) -> None:

        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(self._image,text, _pos(pos), font, 0.5,(0,0,0),2,cv.LINE_AA)

    def end(self) -> None:
        cv.imwrite(self.file, self._image)
