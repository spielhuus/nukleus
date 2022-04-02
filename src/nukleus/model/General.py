from __future__ import annotations
from typing import Dict

from ..SexpParser import SEXP_T
from .SchemaElement import POS_T


class General():
    """
    The general token define general information about the board. This section is required.
    """
    def __init__(self, **kwargs) -> None:
        self.values = kwargs

    @classmethod
    def parse(cls, sexp: SEXP_T) -> General:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype General: The General Object.
        """
        _general: Dict[str, str] = {}

        for token in sexp[1:]:
            _general[token[0]] = token[1]

        return General(**_general)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        return(f'{"  " * indent}(no_connect (at {self.pos[0]} {self.pos[1]}) '
               f'(uuid {self.identifier}))')
