from __future__ import annotations
from typing import cast

from ..SexpParser import SEXP_T


class Net():
    """
    The net token defines a net for the board. This section is required.
    """
    def __init__(self, ordinal: int, netname: str) -> None:
        self.ordinal = ordinal
        self.netname = netname

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Net:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype General: The Net Object.
        """
        _ordinal = int(cast(str, sexp[1]))
        _net_name = str(sexp[2])
        return Net(_ordinal, _net_name)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        return f'{"  " * indent}(net {self.ordinal} {self.netname})'
