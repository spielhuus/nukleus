from __future__ import annotations
from abc import abstractmethod
from typing import TypeVar, Iterator, List, Tuple

from .Typing import POS_T, PTS_T

class SexpNode():
    """Sexp Node Implementation

    This class is used to represent a single node in an s-expressionself.
    It can be used to represent a list of nodes or a single nodeself.
    """
    def __init__(self):
        self.sexp: List[SexpNode|str] = []

    def __contains__(self, key: str) -> bool:
        return len(self[key]) > 0

    def __getitem__(self, key: str|int|slice) -> List[SexpNode]:
        res: List[SexpNode] = []
        for node in self.sexp:
            if isinstance(node, SexpNode) and node.sexp[0] == key:
                res.append(node)
        return res

    def __iter__(self) -> Iterator[SexpNode]:
        return iter([x for x in self.sexp if isinstance(x, SexpNode)])

    def __repr__(self):
        return f'({self.sexp})'

    def __len__(self) -> int:
        return len(self.sexp)

    def values(self) -> List[str]:
        """Return the string value of this Node"""
        res: List[str] = []
        for node in self.sexp:
            if isinstance(node, str):
                res.append(node)
        return res

    def pos(self) -> POS_T:
        """Return the POS_T from this Node"""
        return (float(str(self.sexp[1])), float(str(self.sexp[2])))

    def pts(self) -> PTS_T:
        """Return PTS_T from this node"""
        pts = []
        for _xy in self.sexp:
            if not isinstance(_xy, str) and _xy.get(0, '') == 'xy':
                pts.append((_xy.get(1, 0.0), _xy.get(2, 0.0)))
        return pts

    T = TypeVar("T")
    def get(self, path: int, default: T) -> T:
        """
        Get the value at the position.

        :param path slice: position.
        :param default T: default value.
        :rtype T: Type of default value.
        """
        if len(self.sexp) <= path:
            return default
        #_node = self.__getitem__(path)
        _node = self.sexp[path]
        if _node:
            if isinstance(default, str):
                return str(_node)  # type: ignore
            if isinstance(default, int):
                return int(_node)  # type: ignore
            if isinstance(default, float):
                return float(_node)  # type: ignore

        return default

def load_tree(sexp: str) -> SexpNode:
    """
    Load the sexp string to List

    :param input str: Input string.
    :rtype SEXP_T: The parsed result.
    """
    length = len(sexp)

    def traverse(index: int) -> Tuple[SexpNode, int]:
        res = SexpNode()
        #items = []
        buffer: List[str] = []
        item = sexp[index]

        while item != ")":
            if item in [' ', '\n', '\r']:
                pass
            elif item == '(':
                subtree, index = traverse(index + 1)
                res.sexp.append(subtree)

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
                res.sexp.append("".join(buffer))
            else:
                buffer = []
                while index < length:
                    if sexp[index] == ')':
                        res.sexp.append("".join(buffer))
                        index -= 1
                        break
                    if sexp[index] in [' ', '\n', '\r']:
                        res.sexp.append("".join(buffer))
                        break
                    buffer.append(sexp[index])
                    index += 1

            index += 1
            item = sexp[index]
        return res, index

    return traverse(sexp.find('(')+1)[0]


class SexpVisitor():
    """Visit the SexpNode items."""

    @abstractmethod
    def start(self) -> None:
        """SexpNode callback method."""

    @abstractmethod
    def end(self) -> None:
        """SexpNode callback method."""

    @abstractmethod
    def node(self, name: str, sexp: SexpNode) -> None:
        """SexpNode callback method."""

    def visit(self, sexp: SexpNode, level: int = 0, act_level: int=0) -> None:
        """Visit the sexp nodes."""
        self.start()
        self._visit(sexp, level, act_level)
        self.end()

    def _visit(self, sexp: SexpNode, level: int = 0, act_level: int=0) -> None:
        for node in sexp.sexp:
            if isinstance(node, SexpNode):
                if act_level == level:
                    self.node(str(node.sexp[0]), node)
                else:
                    self._visit(node, level=level, act_level=act_level+1)
