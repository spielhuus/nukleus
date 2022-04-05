from __future__ import annotations
from typing import cast

from ..SexpParser import SEXP_T


class FootprintAttributes():
    """
    Footprint attr token defines the list of attributes of the footprint.
    """
    def __init__(self, attribute_type: str, board_only: bool,
                 exclude_from_pos_files: bool, exclude_from_bom: bool) -> None:
        self.attribute_type: str = attribute_type
        self.board_only: bool = board_only
        self.exclude_from_pos_files: bool = exclude_from_pos_files
        self.exclude_from_bom: bool = exclude_from_bom


    @classmethod
    def parse(cls, sexp: SEXP_T) -> FootprintAttributes:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype General: The FootprintAttributes Object.
        """
        _attribute_type: str = ''
        _board_only: bool = False
        _exclude_from_pos_files: bool = False
        _exclude_from_bom: bool = False

        for token in sexp[1:]:
            if token in ('smd', 'through_hole'):
                _attribute_type = str(token)
            elif token == 'board_only':
                _board_only = True
            elif token == 'exclude_from_pos_files':
                _exclude_from_pos_files = True
            elif token == 'exclude_from_bom':
                _exclude_from_bom = True

        return FootprintAttributes(_attribute_type, _board_only,
                _exclude_from_pos_files, _exclude_from_bom)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        string = f'{"  " * indent}(attr'
        if self.attribute_type and self.attribute_type != '':
            string += f' {self.attribute_type}'
        if self.exclude_from_pos_files and self.exclude_from_pos_files != '':
            string += f' {self.exclude_from_pos_files}'
        if self.exclude_from_bom and self.exclude_from_bom != '':
            string += f' {self.exclude_from_bom}'
        string += ')'
        return string
