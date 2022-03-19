from typing import List

def ffmt(input: float) -> int|float:
    if int(input) == input:
        return int(input)
    return input
