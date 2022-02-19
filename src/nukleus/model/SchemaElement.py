from typing import Tuple, TypeAlias, List

POS_T: TypeAlias = Tuple[float, float]
PTS_T: TypeAlias = List[Tuple[float, float]]

class SchemaElement():
    """  Base element for the schetic items. """
    identifier: str

    def __init__(self, identifier='') -> None:
        self.identifier = identifier
