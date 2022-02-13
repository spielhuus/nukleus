from typing import Optional

from nukleus import Library
from nukleus.model import Junction, POS_T

from .DrawElement import DrawElement


class Dot(DrawElement):
    def __init__(self):
        self.pos = None
        self.element: Optional[Junction] = None

    def _get(self, library: Library, last_pos: POS_T, unit: float):
        self.element = Junction.new()
        self.element.pos = last_pos
        self.pos = last_pos
        return (self, self.element, last_pos)
