from __future__ import annotations

from typing import List, cast

from .SchemaElement import POS_T
from ..SexpParser import SEXP_T


class PcbVia:
    def __init__(
        self,
        via_type: str,
        locked: bool,
        pos: POS_T,
        size: float,
        drill: float,
        layers: str,
        remove_unused_layers: bool,
        keep_end_layers: bool,
        free: bool,
        net: str,
        tstamp: str,
    ) -> None:

        self.via_type: str = via_type
        self.locked: bool = locked
        self.pos: POS_T = pos
        self.size: float = size
        self.drill: float = drill
        self.layers: str = layers
        self.remove_unused_layers: bool = remove_unused_layers
        self.keep_end_layers: bool = keep_end_layers
        self.free: bool = free
        self.net: str = net
        self.tstamp: str = tstamp

    @classmethod
    def parse(cls, sexp: SEXP_T) -> PcbVia:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _via_type: str = str(sexp[1])
        _locked: bool = False
        _pos: POS_T = (0, 0)
        _size: float = 0.0
        _drill: float = 0.0
        _layers: str = ''
        _remove_unused_layers: bool = False
        _keep_end_layers: bool = False
        _free: bool = False
        _net: str = ''
        _tstamp: str = ''

        for token in sexp[1:]:
            if token[0] == 'locked':
                _locked = True
            elif token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
            elif token[0] == 'size':
                _size = float(token[1])
            elif token[0] == 'drill':
                _drill = float(token[1])
            elif token[0] == 'layers':
                _layers = str(token[1])
            elif token[0] == 'remove_unused_layers':
                _remove_unused_layers = True
            elif token[0] == 'keep_end_layers':
                _keep_end_layers = True
            elif token[0] == 'free':
                _free = True
            elif token[0] == 'net':
                _net = str(token[1])
            elif token[0] == 'tstamp':
                _tstamp = str(token[1])
            else:
                raise ValueError(f"Unexpected item: {token}")

        return PcbVia(_via_type, _locked, _pos, _size, _drill, _layers, _remove_unused_layers,
                _keep_end_layers, _free, _net, _tstamp)
