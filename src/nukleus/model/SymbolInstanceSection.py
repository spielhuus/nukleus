from __future__ import annotations

from dataclasses import dataclass
from .SchemaElement import SchemaElement


@dataclass
class SymbolInstanceSection(SchemaElement):
    """ The symbol_instance token defines the per symbol information
        for the entire schematic. This section will only exist in
        schematic files that are the root sheet of a project.

    Parameters:
	    The INSTANCE_PATH attribute is the path to the sheet instance.
        The reference token attribute is a string that defines the reference designator for the symbol instance.
        The unit token attribute is a integer ordinal that defines the symbol unit for the symbol instance. For symbols that do not define multiple units, this will always be 1.
        The value token attribute is a string that defines the value field for the symbol instance.
        The footprint token attribute is a string that defines the LIBRARY_IDENTIFIER for footprint associated with the symbol instance.
    """
    path: str
    reference: str
    unit: str
    value: str
    footprint: str
