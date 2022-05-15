from typing import Optional

from ..Library import Library
from ..ModelSchema import Junction
from ..Typing import POS_T
from .DrawElement import DrawElement


class Dot(DrawElement):
    """Place a junction in the schematic"""

    def __init__(self):
        self.pos = None
        self.element: Optional[Junction] = None

    def _get(self, library: Library, last_pos: POS_T, unit: float):
        self.element = Junction(pos=last_pos)
        self.pos = last_pos
        return (self, self.element, last_pos, None)
