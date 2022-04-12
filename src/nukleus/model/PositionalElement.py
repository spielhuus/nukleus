from __future__ import annotations

from .SchemaElement import SchemaElement, POS_T

def ffmt(number: float) -> int|float:
    """
    convert float to int when there are no decimal places.

    :param number float: The float
    :rtype int|float: The return number.
    """
    if int(number) ==number:
        return int(number)
    return number

class PositionalElement(SchemaElement):
    """ Positional element for the schema items """
    def __init__(self, identifier, pos, angle) -> None:
        self.pos: POS_T = pos
        """The POSITION_IDENTIFIER defines the X and Y coordinates of the element in the sheet."""
        self.angle: float = angle
        """The POSITION_IDENTIFIER defines the angle of rotation of the element in the sheet."""
        super().__init__(identifier)
