from __future__ import annotations

from dataclasses import dataclass
from .SchemaElement import SchemaElement, POS_T


@dataclass
class PositionalElement(SchemaElement):
    """ Positional element for the schema items """
    pos: POS_T
    angle: float
