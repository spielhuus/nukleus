from __future__ import annotations

from .SchemaElement import SchemaElement, POS_T


class PositionalElement(SchemaElement):
    """ Positional element for the schema items """
    identifier: str
    pos: POS_T
    angle: float

    def __init__(self, identifier, pos, angle) -> None:
        self.pos = pos
        self.angle = angle
        super().__init__(identifier)
