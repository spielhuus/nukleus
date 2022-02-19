from __future__ import annotations
from inspect import classify_class_attrs
from typing import List
from dataclasses import dataclass
from .SchemaElement import SchemaElement


@dataclass
class SymbolInstanceSection(SchemaElement):
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
    reference: str
    unit: int
    value: str
    footprint: str


    def __init__(self, **kwargs) -> None:
        self.path = "" if 'path' not in kwargs else kwargs['path']
        self.reference = "" if 'reference' not in kwargs else kwargs['reference']
        self.unit = 0 if 'unit' not in kwargs else kwargs['unit']
        self.value = "" if 'value' not in kwargs else kwargs['value']
        self.footprint = "" if 'footprint' not in kwargs else kwargs['footprint']
        super().__init__(self.path)

    @classmethod
    def parse(cls, sexp) -> SymbolInstanceSection:
        _path: str = ""
        _reference: str = ""
        _unit: int = 0
        _value: str = ""
        _footprint: str = ""

        match sexp:
            case ['path', path, *childs]:
                _path = path
                for item in childs:
                    match item:
                        case ['reference', reference]:
                            _reference = reference
                        case ['unit', unit]:
                            _unit = int(unit)
                        case ['value', value]:
                            _value = value
                        case ['footprint', footprint]:
                            _footprint = footprint
                        case _:
                            raise ValueError(f"unknown path item element {childs}")
            case _:
                raise ValueError(f"unknown path element {sexp}")

        return SymbolInstanceSection(path=_path, reference=_reference, unit=_unit,
                                     value=_value, footprint=_footprint)

    def sexp(self, indent: int=1) -> str:
        strings: List[str] = []
        strings.append(f'{"  " * indent}(path "{self.path}"')
        strings.append(f'{"  " * (indent + 1)}(reference "{self.reference}") (unit {self.unit}) '
                       f'(value "{self.value}") (footprint "{self.footprint}")')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
