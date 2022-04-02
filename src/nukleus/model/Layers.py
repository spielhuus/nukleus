from __future__ import annotations

from typing import List

from ..SexpParser import SEXP_T
from .SchemaElement import POS_T


class Layer:
    def __init__(self, **kwargs) -> None:
        self.ordinal = kwargs.get("ordinal", 0)
        self.canonical_name = kwargs.get("canonical_name", None)
        self.type = kwargs.get("type", None)
        self.user_name = kwargs.get("user_name", None)


class Layers:
    """
    The layers token defines all of the layers used by the board. This section is required.
    """

    def __init__(self) -> None:
        self.layers: List[Layer] = []

    def append(self, layer: Layer) -> None:
        """Append a layer to the list of layers.

        :param layer: layer to append.
        :type layer: Layer
        """
        self.layers.append(layer)

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Layers:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype General: The Layer Object.
        """
        _layers = Layers()

        for token in sexp[1:]:
            _layers.append(
                Layer(
                    ordinal=int(token[0]),
                    canonical_name=token[1],
                    type=token[2],
                    user_name='' if len(token) < 4 else token[3]
                )
            )

        return _layers

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings = []
        strings.append(f'{"  " * indent}(layers')
        for layer in self.layers:
            string = f'{"  " * (indent+1)}({layer.ordinal} {layer.canonical_name} {layer.type}'
            if layer.user_name is not None and layer.user_name != '':
                string += f' {layer.user_name}'
            string += ')'
            strings.append(string)
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
