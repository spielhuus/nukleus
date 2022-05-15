from typing import Optional

from ..Library import Library
from ..ModelSchema import NoConnect
from ..Typing import POS_T
from .DrawElement import DrawElement


class NC(DrawElement):
    """Place a no connect marker in the schematic"""
    def __init__(self):
        self.pos = None
        self.element: Optional[NoConnect] = None

    def _get(self, library: Library, last_pos: POS_T, _: float):
        self.element = NoConnect(pos=last_pos)
        return (self, self.element, last_pos, None)
