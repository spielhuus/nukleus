from enum import Enum


class FillType(Enum):
    """Fill type for the elements."""
    FOREGROUND = 1
    BACKGROUND = 2
    NONE = 3

def get_fill_str(fill_type_type: FillType) -> str:
    """
    get the fill type from the enum.

    :param fill_type FillType: The fill type.
    :rtype str: The type as string.
    """
    if fill_type_type == FillType.FOREGROUND:
        return 'outline'
    if fill_type_type == FillType.BACKGROUND:
        return 'background'
    return 'none'

def get_fill_type(fill_type_type: str) -> FillType:
    """
    Get the fill type from string.

    :param fill_type_type str: The fill type.
    :rtype FillType: Fill type Enum.
    """
    if fill_type_type == 'outline':
        return FillType.FOREGROUND
    if fill_type_type == 'background':
        return FillType.BACKGROUND
    return FillType.NONE
