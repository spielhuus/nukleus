from dataclasses import dataclass
from typing import Tuple, TypeAlias

POS_T: TypeAlias = Tuple[float, float]

@dataclass
class SchemaElement():
    """  Base element for the schetic items. """
    identifier: str
