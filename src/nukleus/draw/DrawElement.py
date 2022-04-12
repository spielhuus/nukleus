from abc import ABC, abstractmethod
from typing import List

from ..Library import Library
from ..model.SchemaElement import POS_T, SchemaElement


class LogicException(Exception):
    """Exception is raised when a wrong logic is applied."""


class PinNotFoundError(Exception):
    """Exception is thrown when a Pin can not be found."""


class DrawElement(ABC):
    """Abstract class for draw elements."""
    pos: POS_T | None = (0, 0)
    element: SchemaElement | None = None

    @abstractmethod
    def _get(self, library: Library, last_pos: POS_T, unit: float) -> List:
        pass
