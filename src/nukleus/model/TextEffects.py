from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List

from ..SexpParser import SEXP_T


class Justify(Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    MIRROR = 5
    CENTER = 6

    @staticmethod
    def get_justify(types: str) -> List[Justify]:
        _lookup = {'left': Justify.LEFT,
                   'right': Justify.RIGHT,
                   'top': Justify.TOP,
                   'bottom': Justify.BOTTOM,
                   'mirror': Justify.MIRROR,
                   'center': Justify.CENTER}
        type_list: List[Justify] = []
        for _type in types:
            type_list.append(_lookup[_type])
        return type_list

    @staticmethod
    def str(justifiers: List[Justify]) -> str:
        _lookup = {Justify.LEFT: 'left',
                   Justify.RIGHT: 'right',
                   Justify.TOP: 'top',
                   Justify.BOTTOM: 'bottom',
                   Justify.MIRROR: 'mirror',
                   Justify.CENTER: 'center'}
        return " ".join([_lookup[x] for x in justifiers])

    @staticmethod
    def halign(type: List[Justify]) -> str:
        for t in type:
            if t == Justify.LEFT:
                return 'left'
            elif t == Justify.RIGHT:
                return 'right'
        return 'center'

    @staticmethod
    def valign(type: List[Justify]) -> str:
        for t in type:
            if t == Justify.TOP:
                return 'top'
            elif t == Justify.BOTTOM:
                return 'bottom'
        return 'center'


@dataclass
class TextEffects():
    face: ''
    font_width: float
    font_height: float
    font_thickness: str
    font_style: str
    justify: List[Justify]
    hidden: bool

    def __init__(self, **kwargs) -> None:
        self.face = kwargs.get('face', '')
        self.font_width = kwargs.get('font_width', 0)
        self.font_height = kwargs.get('font_height', 0)
        self.font_thickness = kwargs.get('font_thickness', '')
        self.font_style = kwargs.get('font_style', '')
        self.justify = kwargs.get('justify', [])
        self.hidden = kwargs.get('hidden', True)

    @classmethod
    def parse(cls, sexp: SEXP_T) -> TextEffects:
        _face = ''
        _font_width = 0
        _font_height = 0
        _font_thickness = ''
        _font_style = ''
        _justify = []
        _hidden = False

        for token in sexp[1:]:
            match token:
                case ['font', ['size', width, height], *style]:
                    _font_width = float(width)
                    _font_height = float(height)
                    _font_style = " ".join(style)
                case ['font', ['size', width, height]]:
                    _font_width = float(width)
                    _font_height = float(height)

                case ['justify', *justify]:
                    _justify = Justify.get_justify(justify)
                case 'hide':
                    _hidden = True
                case _:
                    raise ValueError(f"unknown effects element {token}")

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
