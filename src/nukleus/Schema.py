from typing import List, Type, TypeVar
from .model import SchemaElement, LibrarySymbol, GlobalLabel, LocalLabel, \
                   Symbol, Junction, Wire, NoConnect, ElementList


class Schema():
    """Schema implementation."""

    def __init__(self) -> None:
        self.version: str = ""
        self.generator: str = ""
        self.uuid: str = ""
        self.paper: str = ""

        self.title: str = ""
        self.date: str = ""
        self.rev: str = ""
        self.comment_1: str = ""
        self.comment_2: str = ""
        self.comment_3: str = ""
        self.comment_4: str = ""

        self.elements: List[SchemaElement] = []

    def append(self, element: SchemaElement):
        """
        Add an Element to the Schema.

        :param element: Element to add.
        :type element: SchemaElement
        """
        self.elements.append(element)

    T = TypeVar('T')

    def get_elements(self, class_type: Type[T]) -> List[T]:
        """
        Return a list of elements by class type.

        :param class_type: Element Class Type.
        :type class_type: Type[T]
        :return: List of Elements.
        :rtype: List[T]
        """
        return [x for x in self.elements if isinstance(x, class_type)]

    def getSymbol(self, id: str) -> LibrarySymbol:
        """
        Get a symbol by id. For Kicad schemas this will be the uuid.

        :param id: The identifier.
        :type id: str
        :return: Schema element.
        :rtype: LibrarySymbol
        """
        return [x for x in self.get_elements(LibrarySymbol)
                if x.identifier == id][0]

    def has_symbol(self, id: str) -> bool:
        return len([x for x in self.get_elements(LibrarySymbol)
                if x.identifier == id]) != 0

    def references(self) -> List[str]:
        syms: List[str] = []
        for symbol in self.elements:
            if isinstance(symbol, Symbol) and symbol.has_property("Reference"):
                if self.getSymbol(
                        symbol.library_identifier).extends != 'power':
                    syms.append(symbol.property("Reference").value)
        return sorted(set(syms))

    def __getattr__(self, name, unit=-1) -> List[SchemaElement]|SchemaElement:
        print("schema getattr")
        syms: ElementList = ElementList()
        for symbol in object.__getattribute__(self, 'elements'):
            if isinstance(symbol, Symbol) and symbol.has_property("Reference"):
                if self.getSymbol(
                        symbol.library_identifier).extends != 'power' and \
                symbol.property('Reference').value == name:
                    syms.append(symbol)
        return syms

        raise Exception("symbol and unit not found", name, unit)  # TODO right Exception

    def sexp(self) -> str:
        strings: List[str] = []
        strings.append(f"(kicad_sch (version {self.version}) (generator {self.generator})")
        strings.append(f"(uuid {self.uuid})")
        strings.append(f"(paper \"{self.paper}\")")
        strings.append(f"  (title_block")
        strings.append(f"   (title \"{self.title}\")")
        strings.append(f"   (date \"{self.date}\")")
        strings.append(f"   (rev \"{self.rev}\")")
        if len(self.comment_1) > 0:
            strings.append(f"   (comment 1 \"{self.comment_1}\")")
        if len(self.comment_2) > 0:
            strings.append(f"   (comment 2 \"{self.comment_2}\")")
        if len(self.comment_3) > 0:
            strings.append(f"   (comment 3 \"{self.comment_3}\")")
        if len(self.comment_4) > 0:
            strings.append(f"   (comment 4 \"{self.comment_4}\")")
        strings.append(f"  )")
        strings.append(f"")
        strings.append(f"  (lib_symbols")
        for symbol in self.get_elements(LibrarySymbol):
                strings.append(symbol.sexp(indent=2))
        strings.append('  )')
        strings.append('')
        for junction in self.get_elements(Junction):
                strings.append(junction.sexp())
        strings.append('')
        for no_connect in self.get_elements(NoConnect):
                strings.append(no_connect.sexp())
        strings.append('')
        for wire in self.get_elements(Wire):
                strings.append(wire.sexp())
        strings.append('')
        for label in self.get_elements(LocalLabel):
                strings.append(label.sexp())
        strings.append('')
        for label in self.get_elements(GlobalLabel):
                strings.append(label.sexp())
        strings.append('')
        for symbol in self.get_elements(Symbol):
                strings.append(symbol.sexp())
                strings.append('')
        strings.append('')

        strings.append(f")")
        return "\r\n".join(strings)



    def __str__(self) -> str:
        strings: List[str] = []
        strings.append(f"Schema[\r\nVersion:'{self.version}'\r\n")
        strings.append(f"generator:'{self.generator}'\r\n")
        strings.append(f"paper:'{self.paper}'\r\n")
        strings.append(f"uuid:{self.uuid}\r\n")
        strings.append(f"title: {self.title}\r\n")
        strings.append(f"date: {self.date}\r\n")
        strings.append(f"rev: {self.rev}\r\n")
        strings.append(f"comment 1: '{self.comment_1}'\r\n")
        strings.append(f"comment 2: '{self.comment_2}'\r\n")
        strings.append(f"comment 3: '{self.comment_3}'\r\n")
        strings.append(f"comment 4: '{self.comment_4}'\r\n")

        for e in self.elements:
            strings.append(e.__str__() + '\r\n')
        strings.append("]")
        return "".join(strings)
