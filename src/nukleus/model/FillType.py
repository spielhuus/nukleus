from enum import Enum


class FillType(Enum):
    FOREGROUND = 1
    BACKGROUND = 2
    NONE = 3


def get_fill_str(type: FillType) -> str:
    if type == FillType.FOREGROUND:
        return 'outline'
    elif type == FillType.BACKGROUND:
        return 'background'
    else:
        return 'none'


def get_fill_type(type: str) -> FillType:
    if type == 'outline':
        return FillType.FOREGROUND
    elif type == 'background':
        return FillType.BACKGROUND
    else:
        return FillType.NONE
