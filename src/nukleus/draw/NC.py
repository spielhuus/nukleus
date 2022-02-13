from typing import Optional

from nukleus import Library
from nukleus.model import NoConnect, POS_T

from .DrawElement import DrawElement


class NC(DrawElement):
    def __init__(self):
        self.pos = None
        self.element: Optional[NoConnect] = None

    def _get(self, library: Library, last_pos: POS_T, _: float):
        self.element = NoConnect.new()
        self.element.pos = last_pos
        return (self, self.element, last_pos)
