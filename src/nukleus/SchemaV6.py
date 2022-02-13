"""
Schema implementation for kicad v6 files.
"""

from typing import List, Tuple

import time
from .Schema import Schema
from .model import GraphicItem, LibrarySymbol, LocalLabel, GlobalLabel, \
    Rectangle, \
    StrokeDefinition, Symbol, LibrarySymbol, TextEffects, Wire, Junction, \
    NoConnect, Property, Pin, PinRef, HierarchicalSheetInstance, \
    SymbolInstanceSection, Polyline, FillType, Justify, get_fill_type, rgb

from .SexpParser import load_tree


class SchemaV6(Schema):
    def __init__(self) -> None:
        """
        Create a new SchemaV6 Parser.

        :return: initialized parser.
        :rtype: SchemaV6
        """
        super().__init__()

    def _title_block(self, list) -> None:
        for token in list[1:]:
            match token:
                case ['title', title]:
                    self.title = title
                case ['date', date]:
                    self.date = date
                case ['rev', rev]:
                    self.rev = rev
                case ['comment', '1', comment]:
                    self.comment_1 = comment
                case ['comment', '2', comment]:
                    self.comment_2 = comment
                case ['comment', '3', comment]:
                    self.comment_3 = comment
                case ['comment', '4', comment]:
                    self.comment_4 = comment
                case _:
                    raise ValueError(f"unknown title block element {token}")

    def _pts(self, tokens: List):
        _pts: List[Tuple[float, float]] = []
        for token in tokens[1:]:
            match token:
                case ['xy', x, y]:
                    _pts.append((float(x), float(y)))
                case _:
                    raise ValueError(f"unknown pts element {token}")
        return _pts

    def _pos(self, token: List):
        _x: float = 0
        _y: float = 0
        _angle: int = 0
        match token:
            case ['at', x, y, angle]:
                _x = float(x)
                _y = float(y)
                _angle = float(angle)
            case ['at', x, y]:
                _x = float(x)
                _y = float(y)
            case _:
                raise ValueError(f"unknown pos element {token}")

        return (_x, _y), _angle

    def _effects(self, tokens: List) -> TextEffects:
        _width: float = 0
        _height: float = 0
        _thickness: str = ""
        _style: str = ""
        _justify: List[Justify] = []
        _hidden: bool = False
        for token in tokens[1:]:
            match token:
                case ['font', ['size', width, height], *style]:
                    _width = float(width)
                    _height = float(height)
                    _style = " ".join(style)
                case ['font', ['size', width, height]]:
                    _width = float(width)
                    _height = font(height)

                case ['justify', *justify]:
                    _justify = Justify.get_justify(justify)
                case 'hide':
                    _hidden = True
                case _:
                    raise ValueError(f"unknown effects element {token}")

        return TextEffects(_width, _height, _thickness, _style,
                           _justify, _hidden)

    def _stroke(self, tokens: List) -> StrokeDefinition:
        _width: float = 0
        _type: str = "default"
        _colors: List[str] = []
        for token in tokens[1:]:
            match token:
                case ['width', width]:
                    _width = float(width)
                case ['type', type]:
                    _type = type
                case ["color", *color]:
                    _colors = rgb(*[int(i) for i in color])
                case _:
                    raise ValueError(f"unknown stroke element {token}")

        return StrokeDefinition(_width, _type, _colors)

    def _property(self, tokens: List):
        _key: str = tokens[1]
        _value: str = tokens[2]
        _id: str = ""
        _xy: Tuple(float, float) = (0, 0)
        _angle: float = 0
        _text_effects: List[TextEffects] = []
        for token in tokens[3:]:
            match token:
                case ['id', id]:
                    _id = id
                case ['at', *_]:
                    _xy, _angle = self._pos(token)
                case ['effects', *_]:
                    _text_effects.append(self._effects(token))
                case _:
                    raise ValueError(f"unknown property element {token}")

        return Property(_key, _value, _id, _xy, _angle,
                        None if len(_text_effects) == 0 else _text_effects[0])

    def _pin(self, tokens: List):
        _type: str = tokens[1]
        _style: str = tokens[2]
        _xy: Tuple(float, float) = (0, 0)
        _angle: float = 0
        _length: float = 0
        _name: str = ""
        _name_effect: List[TextEffects] = []
        _number: str = ""
        _number_effect: List[TextEffects] = []
        _hidden = False
        for token in tokens[3:]:
            match token:
                case ['at', *_]:
                    _xy, _angle = self._pos(token)
                case ['length', length]:
                    _length = float(length)
                case ['name', name, *effects]:
                    _name = name
                    _name_effect.append(self._effects(effects[0]))
                case ['number', number, *effects]:
                    _number = number
                    _number_effect.append(self._effects(effects[0]))
                case 'hide':
                    _hidden = True
                case _:
                    raise ValueError(f"unknown property element {token}")
        
        assert len(_name_effect) == 1, \
            f"name effect len is {len(_name_effect)}"
        assert len(_number_effect) == 1, \
            f"number effect len is {len(_number_effect)}"
        return Pin(_type, _style, _xy, _angle, _length, _hidden,
                   (_name, _name_effect[0]),
                   (_number, _number_effect[0]))

    def _polyline(self, tokens: List):
        _pts: List[Tuple[float, float]] = []
        _stroke: List[StrokeDefinition] = []
        _fill: FillType = FillType.NONE
        for token in tokens[1:]:
            match token:
                case ['pts', *_]:
                    _pts = self._pts(token)
                case ['stroke', *_]:
                    _stroke.append(self._stroke(token))
                case ['fill', ['type', fill]]:
                    _fill = get_fill_type(fill)
                case _:
                    raise ValueError(f"unknown polyline element {token}")

        assert len(_stroke) == 1, f"stroke len is {len(_stroke)}"
        return Polyline(_fill, _pts, _stroke[0])

    def _rectangle(self, tokens: List):
        _start_x: float = 0
        _start_y: float = 0
        _end_x: float = 0
        _end_y: float = 0
        _stroke: List[StrokeDefinition] = []
        _fill: FillType = FillType.NONE
        for token in tokens[1:]:
            match token:
                case ['start', x, y]:
                    _start_x = float(x)
                    _start_y = float(y)
                case ['end', x, y]:
                    _end_x = float(x)
                    _end_y = float(y)
                case ['stroke', *_]:
                    _stroke.append(self._stroke(token))
                case ['fill', ['type', fill]]:
                    _fill = get_fill_type(fill)
                case _:
                    raise ValueError(f"unknown rectangle element {token}")

        assert len(_stroke) == 1, f"stroke len is {len(_stroke)}"
        return Rectangle(_fill, _start_x, _start_y, _end_x, _end_y, _stroke[0])

    def _symbol(self, tokens: List):
        _xy: Tuple(float, float) = (0, 0)
        _angle: float = 0
        _lib_id: str = ""
        _mirror: str = ""
        _unit: int = 1
        _uuid: str = ""
        _in_bom: bool = True
        _on_board: bool = True
        _properties: List[Property] = []
        _pins: List[PinRef] = []
        for token in tokens:
            match token:
                case ['lib_id', id]:
                    _lib_id = id
                case ['at', *_]:
                    _xy, _angle = self._pos(token)
                case ['mirror', mirror]:
                    _mirror = mirror
                case ['unit', id]:
                    _unit = int(id)
                case ['in_bom', flag]:
                    _in_bom = flag == "yes"
                case ['on_board', flag]:
                    _on_board = flag == "yes"
                case ['uuid', uuid]:
                    _uuid = uuid
                case ['property', *_]:
                    _properties.append(self._property(token))
                case ['fields_autoplaced']:
                    pass  # TODO
                case ['pin', *items]:
                    _pins.append(PinRef(items[0], items[1][1]))
                case _:
                    raise ValueError(f"unknown symbol element {token}")

        return(Symbol(_uuid, _xy, _angle, _mirror, _lib_id,
                      _unit, _in_bom, _on_board, _properties, _pins))

    def _lib_symbol(self, tokens: List) -> LibrarySymbol:
        _lib_id: str = tokens[1]
        _inherit: str = ''
        _in_bom: bool = True
        _on_board: bool = True
        _properties: List[Property] = []
        _pin_numbers: bool = False
        _offset: float = 0
        _pin_hidden: bool = False
        _pins: List[Pin] = []
        _index = 2
        _sub_symbols: List[LibrarySymbol] = []
        _graphics: List[GraphicItem] = []
        if len(tokens) >= 3 and len(tokens[2]) == 1:
            _inherit = tokens[2][0]
            _index += 1

        for token in tokens[_index:]:
            match token:
                case ['lib_id', id]:
                    _lib_id = id
                case ['pin_numbers', flag]:
                    _pin_numbers = (flag == 'hide')
                case ['pin_names', ['offset', offset]]:
                    _offset = float(offset)
                    _pin_hidden = False
                case ['pin_names', ['offset', offset], 'hide']:
                    _offset = float(offset)
                    _pin_hidden = True
                case ['in_bom', flag]:
                    _in_bom = flag == "yes"
                case ['on_board', flag]:
                    _on_board = flag == "yes"
                case ['property', *_]:
                    _properties.append(self._property(token))
                case ['polyline', *_]:
                    _graphics.append(self._polyline(token))
                case ['rectangle', *_]:
                    _graphics.append(self._rectangle(token))
                case ['symbol', *_]:
                    _sub_symbols.append(self._lib_symbol(token))
                case ['pin', *_]:
                    pin = self._pin(token)
                    _pins.append(pin)
                case _:
                    raise ValueError(f"unknown lib symbol element {token}")

        return(LibrarySymbol(_lib_id, _inherit, _pin_numbers, _offset,
               _pin_hidden, _in_bom, _on_board, _properties, _graphics,
               _pins, _sub_symbols))

    def load(self, file: str) -> None:
        """
        Open a schema from the filesystem.

        :param file: filename
        :type file: str
        """
        with open(file, 'r') as f:
            parsed = load_tree(f.read())
            for item in parsed[1:]:
                match item:
                    case ["version", version]:
                        self.version = str(version)
                    case ["generator", generator]:
                        self.generator = generator
                    case ["uuid", uuid]:
                        self.uuid = uuid
                    case ["paper", paper]:
                        self.paper = paper
                    case ["title_block", *_]:
                        self._title_block(item)
                    case ["lib_symbols", *symbols]:
                        for s in symbols:
                            lib_symbol = self._lib_symbol(s)
                            # TODO print(lib_symbol)
                            self.append(lib_symbol)
                    case ["junction", pos, diameter, *color, uuid]:
                        colors = [str(int) for int in color[0][1:]]
                        _xy, _angle = self._pos(pos)
                        self.append(Junction(
                            uuid[1],
                            _xy, _angle,
                            float(diameter[1]),
                            " ".join(colors)
                        ))
                    case ["no_connect", pos, uuid]:
                        _xy, _angle = self._pos(pos)
                        self.append(NoConnect(
                            uuid[1],
                            _xy, _angle
                        ))
                    case ["bus_entry", pts, size, stroke, uuid]:
                        print(f"bus_entry: {uuid}")
                    case ["wire", pts, stroke, uuid]:
                        self.append(Wire(
                            uuid[1],
                            self._pts(pts),
                            self._stroke(stroke)
                        ))
                    case ["bus", pts, stroke, uuid]:
                        print(f"bus: {uuid}")
                    case ["image", pos, scale, uuid, data]:
                        print(f"image: {uuid}")
                    case ["image", pos, uuid, data]:
                        print(f"image: {uuid}")
                    case ["polyline", pts, stroke, uuid]:
                        print(f"polyline: {uuid}")
                    case ["text", text, pos, effects, uuid]:
                        print(f"text: {uuid}")
                        _xy, _angle = self._pos(pos)
                    case ["label", text, pos, effects, uuid]:
                        _xy, _angle = self._pos(pos)
                        self.append(LocalLabel(
                            uuid[1],
                            _xy, _angle,
                            text,
                            self._effects(effects),  # text effects
                        ))
                    case ["global_label", text, shape, pos, autoplaced,
                          effects, uuid, *properties]:
                        _xy, _angle = self._pos(pos)
                        self.append(GlobalLabel(
                            uuid[1],  # UUID
                            _xy, _angle,  # position
                            text,  # text
                            shape[1],  # shape
                            autoplaced,  # autoplaced
                            self._effects(effects),  # text effects
                            [self._property(x) for x in properties] # properties
                        ))
                    case ["global_label", text, shape, pos, effects,
                          uuid, *properties]:
                        _xy, _angle = self._pos(pos)
                        self.append(GlobalLabel(
                            uuid[1],  # UUID
                            _xy, _angle,  # position
                            text,  # text
                            shape[1],  # shape
                            "No",  # autoplaced
                            self._effects(effects),  # text effects
                            [self._property(x) for x in properties] # properties
                        ))
                    case ["hierarchical_label", text, shape, pos, effects, uuid]:
                        print(f"hierarchical_label: {uuid}")
                    case ["symbol", *items]:
                        self.append(self._symbol(items))
                    case ["sheet", pos, size, autoplaced, stroke, fill, uuid, sheet_name, file_name, *pins]:
                        print(f"sheet: {uuid}")
                        _xy, _angle = self._pos(pos)
                    case ["sheet", pos, size, stroke, fill, uuid, sheet_name, file_name, *pins]:
                        print(f"sheet: {uuid}")
                    case ["sheet_instances", info, *paths]:
                        print(f"sheet_instances: {info}")
                        # HierarchicalSheetInstance(
                        #     "", item[1][1][0], int(item[1][2][1][0]))
                        # )
                    case ["symbol_instances", info, *paths]:
                        print(f"symbol_instances: {len(paths)}")
            #                 self.append(SymbolInstanceSection(
            #                     instance[1][0],
            #                     instance[1][0],
            #                     instance[2][1][0],
            #                     instance[3][1],
            #                     instance[4][1][0],
            #                     instance[5][1][0]

            #                 ))
                    case _:
                        print(f"!!! {item}")
