from abc import ABC
from typing import List, Any, Dict



class Cell(ABC):
    pass

class Frontmatter(Cell):
    def __init__(self, frontmatter: Dict[str, Any]):
        super().__init__()
        self.frontmatter = frontmatter

    def __str__(self) -> str:
        return f'{self.frontmatter}\n'

class Markdown(Cell):
    def __init__(self, text):
        super().__init__()
        self.markdown = text

    def __str__(self) -> str:
        return f'{self.markdown}\n'

class Notebook():

    def __init__(self, frontmatter: Dict[str, Any]):
        self.cells: List[Cell] = []
        self.cells.append(Frontmatter(frontmatter))

    def append(self, cell: Cell):
        self.cells.append(cell)

    def __str__(self) -> str:
        return "\n".join([str(x) for x in self.cells])
