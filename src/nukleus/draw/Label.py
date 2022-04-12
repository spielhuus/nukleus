from typing import Optional

from ..Library import Library
from ..model.LocalLabel import LocalLabel
from ..model.SchemaElement import POS_T
from .DrawElement import DrawElement


class Label(DrawElement):
    """Place a label on the schematic."""

    def __init__(self, text: str):
        self.pos = None
        self.text = text
        self.element: Optional[LocalLabel] = None
        self.angle: float = 0.0

    def _get(self, library: Library, last_pos: POS_T, _: float):
        self.element = LocalLabel(
            text=self.text, pos=last_pos, angle=self.angle)
        return (self, self.element, last_pos, None)

    def rotate(self, angle: float):
        """
        Rotate the symbol.

        :param angle float: Rotation angle in degrees.
        """
        self.angle = angle
        return self
