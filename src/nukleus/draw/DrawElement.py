from abc import ABC, abstractmethod

from typing import List

from nukleus import Library
from nukleus.model import SchemaElement, POS_T

def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a


class LogicException(Exception):
    pass


class PinNotFoundError(Exception):
    pass


class DrawElement(ABC):
    pos: POS_T|None = (0, 0)
    element: SchemaElement|None = None

    @abstractmethod
    def _get(self, library: Library, last_pos: POS_T, unit: float) -> List:
        pass
