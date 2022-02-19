from __future__ import annotations

from dataclasses import dataclass

from .SchemaElement import SchemaElement


@dataclass
class HierarchicalSheetInstance(SchemaElement):
    """ The symbol_instance token defines the per symbol information
        for the entire schematic. This section will only exist in
        schematic files that are the root sheet of a project.

    Parameters:
	    The INSTANCE_PATH attribute is the path to the sheet instance.
        The reference token attribute is a string that defines the reference designator for the symbol instance.
        The unit token attribute is a integer ordinal that defines the symbol unit for the symbol instance. For symbols that do not define multiple units, this will always be 1.
        The value token attribute is a string that defines the value field for the symbol instance.
        The footprint token attribute is a string that defines the LIBRARY_IDENTIFIER for footprint associated with the symbol instance.
    """
    path: str
    page: int

    def __init__(self, **kwargs) -> None:
        self.path = "" if 'path' not in kwargs else kwargs['path']
        self.page = 0 if 'page' not in kwargs else kwargs['page']
        super().__init__(self.path)

    @classmethod
    def parse(cls, sexp) -> HierarchicalSheetInstance:
        _path: str = ""
        _page: int = 0

        match sexp:
            case ['path', path, *childs]:
                _path = path
                for item in childs:
                    match item:
                        case ['page', page]:
                            _page = int(page)
                        case _:
                            raise ValueError(
                                f"unknown path item element {childs}")
            case _:
                raise ValueError(f"unknown path element {sexp}")

        return HierarchicalSheetInstance(path=_path, page=_page)

    def sexp(self, indent: int = 1) -> str:
        return f'{"  " * indent}(path "{self.path}" (page "{self.page}"))'
