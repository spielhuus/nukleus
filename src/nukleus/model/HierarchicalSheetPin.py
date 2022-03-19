from __future__ import annotations

from typing import List, cast

from nukleus.model.TextEffects import TextEffects

from .Utils import ffmt
from .SchemaElement import POS_T
from .PositionalElement import PositionalElement
from ..SexpParser import SEXP_T


class HierarchicalSheetPin(PositionalElement):
    """
    The pin token in a sheet object defines an electrical connection between
    the sheet in a schematic with the hierarchical label defined in the
    associated schematic file.
    """

    def __init__(self, **kwargs) -> None:
        self.name: str =  kwargs.get('name', '')
        """The "NAME" attribute defines the name of the sheet pin. It must have
        an identically named hierarchical label in the associated schematic file."""
        self.pin_type: str =  kwargs.get('pin_type', '')
        """The electrical connect type token defines the type of electrical
        connect made by the sheet pin."""
        self.text_effects: TextEffects =  kwargs.get('text_effects', TextEffects())
        """The TEXT_EFFECTS section defines how the pin name text is drawn."""
        super().__init__(kwargs.get('identifier', None),
                         kwargs.get('pos', (0, 0)),
                         kwargs.get('angle', 0))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> HierarchicalSheetPin:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype HierarchicalSheet: The HierarchicalSheet Object.
        """
        _name: str = str(sexp[1])
        _pin_type: str = ''
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _text_effects: TextEffects = TextEffects()
        _identifier: str|None = None

        for token in sexp[2:]:
            if token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'uuid':
                _identifier = token[1]
            elif token[0] == 'effects':
                _text_effects = TextEffects.parse(cast(SEXP_T, token))
            elif token in ('input', 'output', 'bidirectional', 'tri_state', 'passive'):
                _pin_type = token
            else:
                raise ValueError(f"unknown HierarchicalSheetPin element {token}")

        return HierarchicalSheetPin(name=_name, pin_type=_pin_type, pos=_pos, angle=_angle,
                                    text_effects=_text_effects, identifier=_identifier)

    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(pin "{self.name}" {self.pin_type} '
                       f'(at {ffmt(self.pos[0])} {ffmt(self.pos[1])} {ffmt(self.angle)})')
        strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
