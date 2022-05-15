from abc import ABC, abstractmethod
from typing import List

from .ModelBase import Justify, rgb
from .Typing import POS_T, PTS_T


class AbstractPlot(ABC):
    """
    Abstract base class for plotting.
    """

    def start(self) -> None:
        """Start plot"""

    def end(self) -> None:
        """Plot end"""

    @abstractmethod
    def polyline(self, pts: PTS_T, width: float, color: rgb, fill: rgb | None = None) -> None:
        """
        Plot a polyline.

        :param pts PTS_T: The points of the polyline.
        """
        raise NotImplementedError

    @abstractmethod
    def rectangle(self, start: POS_T, end: POS_T, width: float, color: rgb, fill: rgb | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def line(self, pts: PTS_T, width: float, color: rgb) -> None:
        raise NotImplementedError

    @abstractmethod
    def circle(self, pos: POS_T, radius: float, width: float, color: rgb, fill: rgb | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def arc(self, pos: POS_T, radius: float, start: float, end: float, width: float,
            color: rgb, fill: rgb | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def text(self, pos: POS_T, text: str, font_height: float, font_with: float,
             face: str, rotate: float, style: str, thickness: float,
             color: rgb, align: List[Justify]) -> None:
        raise NotImplementedError
