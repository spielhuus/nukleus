from __future__ import annotations

from dataclasses import dataclass
from typing import List
from enum import Enum


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
    font_width: float
    font_height: float
    font_thickness: str
    font_style: str
    justify: List[Justify]
    hidden: bool

    @classmethod
    def new(cls) -> TextEffects:
        return TextEffects(0, 0, '', '', [], False)

    def sexp(self, indent=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        string = f'{"  " * indent}(effects (font (size '
        string += f'{self.font_height:g} {self.font_width:g})'
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
