from __future__ import annotations

from dataclasses import dataclass

from .SchemaElement import SchemaElement


@dataclass
class HierarchicalSheetInstance(SchemaElement):
    """ Hierarchical sheet instance """
    path: str
    page: int
