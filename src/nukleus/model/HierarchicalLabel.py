from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List

import uuid

from nukleus.model.TextEffects import TextEffects

from .PositionalElement import PositionalElement
from .TextEffects import TextEffects


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
        Get the shape type as string.

        Parameters
        ----------
        shape : HierarchicalLabelShape
            The shape type.

        Returns
        -------
        str
            The shape type as string.
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
        Get the shape Enum type from string.

        Parameters
        ----------
        shape : str
            The shape string.

        Returns
        -------
        HierarchicalLabelShape
            The shape enum type.
        """
        mappings = {
            'input': HierarchicalLabelShape.INPUT,
            'output': HierarchicalLabelShape.OUTPUT,
            'bidirectional': HierarchicalLabelShape.BIDIRECTIONAL,
            'tri_state': HierarchicalLabelShape.TRI_STATE,
            'passive': HierarchicalLabelShape.PASSIVE,
            }
        return mappings[shape]

@dataclass
class HierarchicalLabel(PositionalElement):
    """
    The hierarchical_label section defines labels that are used by hierarchical
    sheets to define connections between sheet in hierarchical designs. This
    section will not exist if no global labels are defined in the schematic.
    """
    text: str
    shape: HierarchicalLabelShape
    text_effects: TextEffects

    @classmethod
    def new(cls) -> HierarchicalLabel:
        """
        Create a new HierarchicalLabel instance

        Returns: HierarchicalLabel
        """
        return HierarchicalLabel(str(uuid.uuid4()), (0, 0), 0, "",
                                 HierarchicalLabelShape.BIDIRECTIONAL,
                                 TextEffects.new())

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
                   f'(at {self.pos[0]} {self.pos[1]})')
        strings.append(string)
        strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
