from __future__ import annotations

from typing import List, cast

from .SchemaElement import POS_T
from ..SexpParser import SEXP_T


class PcbSegment:
    def __init__(
        self,
        start: POS_T,
        end: POS_T,
        width: float,
        layer: str,
        locked: bool,
        net: str,
        tstamp: str,
    ) -> None:

        self.start: POS_T = start
        self.end: POS_T = end
        self.width: float = width
        self.layer: str = layer
        self.locked: bool = locked
        self.net: str = net
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> PcbSegment:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _start: POS_T = (0, 0)
        _end: POS_T = (0, 0)
        _width: float = 0.0
        _layer: str = ''
        _locked: bool = False
        _net: str = ''
        _tstamp: str = ''

        for token in sexp[1:]:
            if token[0] == 'start':
                _start = (float(token[1]), float(token[2]))
            elif token[0] == 'end':
                _end = (float(token[1]), float(token[2]))
            elif token[0] == 'width':
                _width = float(token[1])
            elif token[0] == 'layer':
                _layer = token[1]
            elif token[0] == 'locked':
                _locked = True
            elif token[0] == 'net':
                _net = token[1]
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return PcbSegment(_start, _end, _width, _layer, _locked, _net, _tstamp)
