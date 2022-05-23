from __future__ import annotations

from dataclasses import dataclass, field
from abc import ABC
from enum import Enum
from typing import Any, Dict, List, Tuple


@dataclass(kw_only=True)
class TitleBlock():
    """Schema title block"""
    title: str = ""
    """The title of the schema."""
    date: str = ""
    """Revision Date"""
    rev: str = ""
    """Revision string"""
    company: str = ""
    """Company string"""
    comment: Dict[int, str] = field(default_factory=dict)
    """Schema comments"""


class rgb():
    def __init__(self, r: float, g: float, b: float, a: float):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def get_hex(self) -> str:
        return f"#{hex(int(self.r*255))}{hex(int(self.g*255))}{hex(int(self.b*255))}{hex(int(self.a*100))}"

    def get(self) -> Tuple[float, float, float, float]:
        return (self.r, self.g, self.b, self.a)

    def __eq__(self, other: Any) -> Any:
        return self.r == other.r and \
            self.g == other.g and \
            self.b == other.b and \
            self.a == other.a


class FillType(Enum):
    """Fill type for the elements."""
    FOREGROUND = 1
    BACKGROUND = 2
    NONE = 3


def get_fill_str(fill_type_type: FillType) -> str:
    """
    get the fill type from the enum.

    :param fill_type FillType: The fill type.
    :rtype str: The type as string.
    """
    if fill_type_type == FillType.FOREGROUND:
        return 'outline'
    if fill_type_type == FillType.BACKGROUND:
        return 'background'
    return 'none'


def get_fill_type(fill_type_type: str) -> FillType:
    """
    Get the fill type from string.

    :param fill_type_type str: The fill type.
    :rtype FillType: Fill type Enum.
    """
    if fill_type_type == 'outline':
        return FillType.FOREGROUND
    if fill_type_type == 'background':
        return FillType.BACKGROUND
    return FillType.NONE


class Justify(Enum):
    """Text orientation."""
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    MIRROR = 5
    CENTER = 6

    @staticmethod
    def get_justify(types: List[str]) -> List[Justify]:
        """
        Parse the justify string.

        :param types List[str]: The justify array.
        :rtype List[Justify]: parsed list.
        """
        _lookup = {'left': Justify.LEFT,
                   'right': Justify.RIGHT,
                   'top': Justify.TOP,
                   'bottom': Justify.BOTTOM,
                   'mirror': Justify.MIRROR,
                   'center': Justify.CENTER}
        type_list: List[Justify] = []
        for _type in types:
            type_list.append(_lookup[str(_type)])
        return type_list

    @staticmethod
    def string(justifiers: List[Justify]) -> str:
        """
        Justifiers as string.

        :param justifiers List[Justify]: The justifiers.
        :rtype str: Justifiers as string.
        """
        _lookup = {Justify.LEFT: 'left',
                   Justify.RIGHT: 'right',
                   Justify.TOP: 'top',
                   Justify.BOTTOM: 'bottom',
                   Justify.MIRROR: 'mirror',
                   Justify.CENTER: 'center'}
        return " ".join([_lookup[x] for x in justifiers])

    @staticmethod
    def halign(justifiers: List[Justify]) -> str:
        """
        Horizontal align.

        :param justifiers List[Justify]: The List of justifiers.
        :rtype str: aling [left, right, center]
        """
        for justify in justifiers:
            if justify == Justify.LEFT:
                return 'left'
            if justify == Justify.RIGHT:
                return 'right'
        return 'center'

    @staticmethod
    def valign(justifiers: List[Justify]) -> str:
        """
        Vertical align.

        :param justifiers List[Justify]: The List of justifiers.
        :rtype str: aling [top, bottom, center]
        """
        for justify in justifiers:
            if justify == Justify.TOP:
                return 'top'
            if justify == Justify.BOTTOM:
                return 'bottom'
        return 'center'


@dataclass(kw_only=True)
class TextEffects():
    """The text effects definition."""

    face: str = ''
    """The optional face token indicates the font family.
    It should be a TrueType font family name."""
    font_width: float = 0
    """The font width."""
    font_height: float = 0
    """The font height."""
    font_thickness: float = 0
    """The font thickness."""
    font_style: List[str] = field(default_factory=list)
    """The font style."""
    justify: List[Justify] = field(default_factory=list)
    """The font justify."""
    hidden: bool = True
    """True if the text is hidden."""
    color: rgb = rgb(0, 0, 0, 0)
    """Text color."""

@dataclass(kw_only=True)
class StrokeDefinition():
    """
    The stroke token defines how the outlines of graphical objects are drawn.
    """

    width: float = 0
    """The width token attribute defines the line width of the graphic object."""
    stroke_type: str = 'default'
    """The type token attribute defines the line style of the graphic object.
    Valid stroke line styles are:
    -dash
    -dash_dot
    -dash_dot_dot (version 7)
    -dot
    -default
    -solid"""
    color: rgb = rgb(0, 0, 0, 0)
    """The color token attributes define the line red, green, blue, and alpha color settings."""


class BaseElement(ABC):
    """Abstract class for the Elements"""
