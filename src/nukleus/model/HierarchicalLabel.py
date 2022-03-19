from __future__ import annotations

from enum import Enum
from typing import List, cast
from nukleus.SexpParser import SEXP_T

from nukleus.model.TextEffects import TextEffects

from .SchemaElement import POS_T
from .PositionalElement import PositionalElement
from .TextEffects import TextEffects
from .Utils import ffmt

class HierarchicalLabelShape(Enum):
    """
    Shape tokens global labels, hierarchical labels, and hierarchical sheet pins.
    """
    INPUT = 1
    OUTPUT = 2
    BIDIRECTIONAL = 3
    TRI_STATE = 4
    PASSIVE = 5

    @classmethod
    def str(cls, shape: HierarchicalLabelShape) -> str:
        """
        HierarchicalLabel shape as string.

        :param shape HierarchicalLabelShape: The Shape.
        :rtype str: Shape as string.
        """
        mappings = {
            HierarchicalLabelShape.INPUT: 'input',
            HierarchicalLabelShape.OUTPUT: 'output',
            HierarchicalLabelShape.BIDIRECTIONAL: 'bidirectional',
            HierarchicalLabelShape.TRI_STATE: 'tri_state',
            HierarchicalLabelShape.PASSIVE: 'passive',
            }
        return mappings[shape]

    @classmethod
    def shape(cls, shape: str) -> HierarchicalLabelShape:
        """
        Parse HierarchicalLabel.

        :param shape str: Shape as string.
        :rtype HierarchicalLabelShape: Shape Enum.
        """
        mappings = {
            'input': HierarchicalLabelShape.INPUT,
            'output': HierarchicalLabelShape.OUTPUT,
            'bidirectional': HierarchicalLabelShape.BIDIRECTIONAL,
            'tri_state': HierarchicalLabelShape.TRI_STATE,
            'passive': HierarchicalLabelShape.PASSIVE,
            }
        return mappings[shape]

class HierarchicalLabel(PositionalElement):
    """
    The hierarchical_label section defines labels that are used by hierarchical
    sheets to define connections between sheet in hierarchical designs. This
    section will not exist if no global labels are defined in the schematic.
    """
    def __init__(self, **kwargs) -> None:
        self.text: str =  kwargs.get('text', '')
        """The TEXT is a quoted string that defines the hierarchical label."""
        self.shape: HierarchicalLabelShape = kwargs.get('shape', HierarchicalLabelShape.INPUT)
        """The shape token attribute defines the way the hierarchical label
        is drawn. See table below for hierarchical label shapes."""
        self.text_effects: TextEffects =  kwargs.get('text_effects', TextEffects())
        """The TEXT_EFFECTS section defines how the hierarchical label text is drawn."""
        super().__init__(kwargs.get('identifier', None),
                         kwargs.get('pos', ((0, 0), (0, 0))),
                         kwargs.get('angle', 0))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> HierarchicalLabel:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype HierarchicalLabel: The HierarchicalLabel Object.
        """
        _text: str = str(sexp[1])
        _shape: HierarchicalLabelShape|None = None
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
            elif token[0] == 'shape':
                _shape = HierarchicalLabelShape.shape(token[1])
            elif token[0] == 'effects':
                _text_effects = TextEffects.parse(cast(SEXP_T, token))
            else:
                raise ValueError(f"unknown hierarchical_label element {token}")

        return HierarchicalLabel(text=_text, shape=_shape, pos=_pos, angle=_angle,
                text_effects=_text_effects, identifier=_identifier)

    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        string = ''
        string += (f'{"  " * indent}(hierarchical_label \"{self.text}\" '
                   f'(shape {HierarchicalLabelShape.str(self.shape)}) '
                   f'(at {ffmt(self.pos[0])} {ffmt(self.pos[1])} {ffmt(self.angle)})')
        strings.append(string)
        strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
