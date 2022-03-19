from __future__ import annotations

from .SchemaElement import SchemaElement


class PositionalElement(SchemaElement):
    """ Positional element for the schema items """
    def __init__(self, identifier, pos, angle) -> None:
        self.pos = pos
        """The POSITION_IDENTIFIER defines the X and Y coordinates of the element in the sheet."""
        self.angle = angle
        """The POSITION_IDENTIFIER defines the angle of rotation of the element in the sheet."""
        super().__init__(identifier)
