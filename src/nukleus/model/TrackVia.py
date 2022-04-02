from __future__ import annotations

from typing import List

from ..SexpParser import SEXP_T
from .SchemaElement import POS_T


class TrackVia:
    """
    The via token defines a track via.
    """
    def __init__(self, via_type: str, locked: bool, at: POS_T, size: float, drill: float,
            layers: List[str], remove_unused_layers: bool, keep_end_layers: bool,
            free: bool, net: int, tstamp: str) -> None:

        self.via_type: str = via_type
        self.locked: bool = locked
        self.at: POS_T = at
        self.size: float = size
        self.drill: float = drill
        self.layers: List[str] = layers
        self.remove_unused_layers: bool = remove_unused_layers
        self.keep_end_layers: bool = keep_end_layers
        self.free: bool = free
        self.net: int = net
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> TrackVia:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype General: The TrackSegment Object.
        """
        _via_type: str = ''
        _locked: bool = False
        _at: POS_T = (0, 0)
        _size: float = 0.0
        _drill: float = 0.0
        _layers: List[str] = []
        _remove_unused_layers: bool = False
        _keep_end_layers: bool = False
        _free: bool = False
        _net: int = 0
        _tstamp: str = ''

        for token in sexp[1:]:
            if token[0] == 'type':
                _via_type = token[1]
            elif token[0] == 'locked':
                _locked = True
            elif token[0] == 'at':
                _at = (float(token[1]), float(token[2]))
            elif token[0] == 'size':
                _size = float(token[1])
            elif token[0] == 'drill':
                _drill = float(token[1])
            elif token[0] == 'layers':
                _layers = token[1:]
            elif token[0] == 'remove_unused_layers':
                _remove_unused_layers = True
            elif token[0] == 'keep_end_layers':
                _keep_end_layers = True
            elif token[0] == 'free':
                _free = True
            elif token[0] == 'net':
                _net = int(token[1])
            elif token[0] == 'tstamp':
                _tstamp = token[1]
            else:
                raise ValueError(f'Unknown token {token[0]}')

        return TrackVia(_via_type, _locked, _at, _size, _drill, _layers, _remove_unused_layers,
                            _keep_end_layers, _free, _net, _tstamp)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        string = f'{"  " * indent}(via '
        if self.via_type:
            string += f'(type {self.via_type}) '
        if self.locked:
            string += '(locked) '
        string += f'(at {self.at[0]} {self.at[1]}) '
        string += f'(size {self.size}) (drill {self.drill}) '
        string += '(layers'
        for layer in self.layers:
            string += f' "{layer}"'
        string += ') '
        if self.remove_unused_layers:
            string += '(remove_unused_layers) '
        if self.keep_end_layers:
            string += '(keep_end_layers) '
        if self.free:
            string += '(free) '
        string += f'(net {self.net}) (tstamp {self.tstamp}))'
        return string
