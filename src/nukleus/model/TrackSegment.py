from __future__ import annotations

from ..SexpParser import SEXP_T
from .SchemaElement import POS_T


class TrackSegment:
    """
    The segment token defines a track segment.
    """
    def __init__(self, start: POS_T, end: POS_T, width: float, layer: str,
            locked: bool, net: int, tstamp: str) -> None:
        self.start: POS_T = start
        self.end: POS_T = end
        self.width: float = width
        self.layer: str = layer
        self.locked: bool = locked
        self.net: int = net
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> TrackSegment:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype General: The TrackSegment Object.
        """
        _start: POS_T = (0, 0)
        _end: POS_T = (0, 0)
        _width: float = 0.0
        _layer: str = ''
        _locked: bool = False
        _net: int = 0
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
                _net = int(token[1])
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            else:
                raise ValueError(f'Unknown token {token[0]}')

        return TrackSegment(_start, _end, _width, _layer, _locked, _net, _tstamp)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        string = f'{"  " * indent}(segment (start {self.start[0]} {self.start[1]}) '
        string += f'(end {self.end[0]} {self.end[1]}) '
        string += f'(width {self.width}) (layer "{self.layer}") '
        if self.locked:
            string += f'(locked {self.locked}) '
        string += f'(net {self.net}) (tstamp {self.tstamp}))'
        return string
