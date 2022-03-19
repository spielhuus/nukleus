from __future__ import annotations

from enum import Enum
from typing import Any, List, cast

from ..SexpParser import SEXP_T


class Justify(Enum):
    """Text orientation."""
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    MIRROR = 5
    CENTER = 6

    @staticmethod
    def get_justify(types: SEXP_T) -> List[Justify]:
        """
        Parse the justify string.

        :param types SEXP_T: [TODO:description]
        :rtype List[Justify]: [TODO:description]
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
    def str(justifiers: List[Justify]) -> str:
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


class TextEffects():
    """The text effects definition."""
    def __init__(self, **kwargs) -> None:
        self.face: str = kwargs.get('face', '')
        """The optional face token indicates the font family.
        It should be a TrueType font family name."""
        self.font_width: float = kwargs.get('font_width', 0)
        """The font width."""
        self.font_height: float = kwargs.get('font_height', 0)
        """The font height."""
        self.font_thickness: str = kwargs.get('font_thickness', '')
        """The font thickness."""
        self.font_style: str = kwargs.get('font_style', '')
        """The font style."""
        self.justify: List[Justify] = kwargs.get('justify', [])
        """The font justify."""
        self.hidden: bool = kwargs.get('hidden', True)
        """True if the text is hidden."""

    @classmethod
    def parse(cls, sexp: SEXP_T) -> TextEffects:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype TextEffects: The TextEffects Object.
        """
        _face = ''
        _font_width = 0
        _font_height = 0
        _font_thickness = ''
        _font_style = ''
        _justify = []
        _hidden = False

        for token in sexp[1:]:
            if token[0] == 'font' and token[1][0] == 'size':
                _font_width = float(token[1][1])
                _font_height = float(token[1][2])
                if len(token) > 2 and token[2][0] == 'thickness':
                    _font_thickness = token[2][1]
                    if len(token) > 4:
                        _font_style = " ".join(token[3:])
                elif len(token) > 2:
                    _font_style = " ".join(token[2:])
            elif token[0] == 'justify':
                _justify = Justify.get_justify(cast(SEXP_T, token[1:]))
            elif token == 'hide':
                _hidden = True
            else:
                raise ValueError(f"unknown TextEffects element {token}")

        return TextEffects(face=_face, font_width=_font_width, font_height=_font_height,
                           font_thickness=_font_thickness, font_style=_font_style,
                           justify=_justify, hidden=_hidden)

    def sexp(self, indent=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        string = f'{"  " * indent}(effects '
        string += '' if self.face == '' else f'(face {self.face}) '
        string += f'(font (size {self.font_height:g} {self.font_width:g})'
        if self.font_thickness != '':
            string += f' (thickness {self.font_thickness})'
        if self.font_style != '':
            string += f' {self.font_style}'
        string += ')'
        if len(self.justify) > 0:
            string += f' (justify {Justify.str(self.justify)})'
        if self.hidden:
            string += ' hide'
        string += ')'
        return string

    def __eq__(self, other: Any) -> Any:
        return (self.face == other.face and
               self.font_width == other.font_width and
               self.font_height == other.font_height and
               self.font_thickness == other.font_thickness and
               self.font_style == other.font_style and
               self.justify == other.justify and
               self.hidden == other.hidden)
