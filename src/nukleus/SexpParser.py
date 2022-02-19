from typing import List, Union, Tuple, TypeAlias

SEXP_T: TypeAlias = List[str|List[str]]

def load_tree(input: str) -> SEXP_T:
    length = len(input)

    def tr(index: int) -> Tuple[SEXP_T, int]:
        res: SEXP_T = []
        item = input[index]

        while item != ")":
            if item in [' ', '\n', '\r']:
                pass
            elif item == '(':
                subtree: SEXP_T = []
                subtree, index = tr(index + 1)
                res.append(subtree)
            elif item == '"':
                buffer = []
                index += 1
                while index < length:
                    if input[index] == '"':
                        break
                    elif input[index] == '\\':
                        buffer.append(input[index])
                        index += 1
                    buffer.append(input[index])
                    index += 1
                res.append("".join(buffer))
            else:
                buffer = []
                while index < length:
                    if input[index] == ')':
                        res.append("".join(buffer))
                        index -= 1
                        break
                    elif input[index] in [' ', '\n', '\r']:
                        res.append("".join(buffer))
                        break
                    buffer.append(input[index])
                    index += 1

            index += 1
            item = input[index]
        return res, index
    
    return tr(input.find('(')+1)[0]
