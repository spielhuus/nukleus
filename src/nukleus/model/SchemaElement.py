from typing import Tuple, TypeAlias, List
import uuid

POS_T: TypeAlias = Tuple[float, float]
PTS_T: TypeAlias = List[POS_T]

class SchemaElement():
    """  Base element for the schetic items. """
    def __init__(self, identifier: str|None=None) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        self.identifier = identifier
        """The UNIQUE_IDENTIFIER defines the universally unique identifier for the pin."""
