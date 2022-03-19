from __future__ import annotations
from typing import List, Tuple, TypeAlias

SEXP_T: TypeAlias = List[str|List[str]]

def load_tree(sexp: str) -> SEXP_T:
    """
    Load the sexp string to List

    :param input str: Input string.
    :rtype SEXP_T: The parsed result.
    """
    length = len(sexp)

    def traverse(index: int) -> Tuple[SEXP_T, int]:
        res: SEXP_T = []
        item = sexp[index]

        while item != ")":
            if item in [' ', '\n', '\r']:
                pass
            elif item == '(':
                subtree: SEXP_T = []
                subtree, index = traverse(index + 1)
                res.append(subtree)
            elif item == '"':
                buffer = []
                index += 1
                while index < length:
                    if sexp[index] == '"':
                        break
                    if sexp[index] == '\\':
                        buffer.append(sexp[index])
                        index += 1
                    buffer.append(sexp[index])
                    index += 1
                res.append("".join(buffer))
            else:
                buffer = []
                while index < length:
                    if sexp[index] == ')':
                        res.append("".join(buffer))
                        index -= 1
                        break
                    if sexp[index] in [' ', '\n', '\r']:
                        res.append("".join(buffer))
                        break
                    buffer.append(sexp[index])
                    index += 1

            index += 1
            item = sexp[index]
        return res, index

    return traverse(sexp.find('(')+1)[0]
