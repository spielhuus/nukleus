from typing import Optional

from nukleus import Library
from nukleus.model import LocalLabel, POS_T

from .DrawElement import DrawElement


class Label(DrawElement):
    """Place a label on the schematic."""
    def __init__(self, text: str):
        self.pos = None
        self.text = text
        self.element: Optional[LocalLabel] = None
        self.angle: float = 0.0
    def _get(self, library: Library, last_pos: POS_T, _: float):
        self.element = LocalLabel(text=self.text, pos=last_pos, angle=self.angle)
        return (self, self.element, last_pos, None)

    def rotate(self, angle: float):
        """
        Rotate the symbol.

        :param angle float: Rotation angle in degree.
        """
        self.angle = angle
        return self
