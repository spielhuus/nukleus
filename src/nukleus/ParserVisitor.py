from typing import Any, Dict, List, cast

from .AbstractParser import AbstractParser
from .ModelBase import (Justify, StrokeDefinition, TextEffects, TitleBlock,
                        get_fill_type, rgb)
from .ModelPcb import *
from .ModelSchema import (Arc, Bus, BusEntry, Circle, GlobalLabel,
                          GraphicalLine, GraphicalText, GraphicItem,
                          HierarchicalLabel, HierarchicalLabelShape,
                          HierarchicalSheet, HierarchicalSheetInstance,
                          HierarchicalSheetPin, Junction, LibrarySymbol,
                          LocalLabel, NoConnect, Pin, PinRef, Polyline,
                          Property, Rectangle, Symbol, SymbolInstance, Wire)
from .SexpParser import SexpNode, SexpVisitor


class ParserVisitor(SexpVisitor):
    """Abstract Sexp Parser"""

    def __init__(self, consumer: AbstractParser):
        self.libraries: Dict[str, LibrarySymbol] = {}
        self.consumer = consumer

        self.version = ''
        self.generator = ''
        self.paper = ''
        self.uuid = ''

    @staticmethod
    def _rgb(sexp: SexpNode) -> rgb:
        return rgb(*[float(str(x)) for x in sexp['color'][0].values()[1:]])

    @staticmethod
    def _get_text_effects(sexp: SexpNode) -> TextEffects:
        result: Dict[str, Any] = {}
        if 'font' in sexp:
            font = sexp['font'][0]
            if 'face' in font:
                result['face'] = font['face'][0].get(1, '')
            if 'size' in font:
                result['font_width'] = font['size'][0].get(1, 0.0)
                result['font_height'] = font['size'][0].get(2, 0.0)
            if 'thickness' in font:
                result['font_thickness'] = font['thickness'][0].get(1, 0.0)

            font_style = []
            if 'bold' in font.values():
                font_style.append('bold')
            if 'italic' in font.values():
                font_style.append('italic')
            result['font_style'] = font_style

        if 'justify' in sexp:
            result['justify'] = Justify.get_justify(
                sexp['justify'][0].values()[1:])
        result['hidden'] = 'hide' in sexp.values()
        return TextEffects(**result)

    @staticmethod
    def _get_stroke_definition(sexp: SexpNode) -> StrokeDefinition:
        result: Dict[str, Any] = {}
        if 'width' in sexp:
            result['width'] = sexp['width'][0].get(1, 0.0)
        if 'type' in sexp:
            result['stroke_type'] = sexp['type'][0].get(1, '')
        if 'color' in sexp:
            result['color'] = ParserVisitor._rgb(sexp)
        return StrokeDefinition(**result)

    @staticmethod
    def _get_property(sexp: SexpNode) -> Property:
        result: Dict[str, Any] = {}
        if 'at' in sexp:
            result['pos'] = sexp['at'][0].pos()
        result['angle'] = sexp['at'][0].get(3, 0.0)
        result['key'] = sexp.get(1, '')
        result['value'] = sexp.get(2, '')
        result['id'] = sexp['id'][0].get(1, 0)
        if 'effects' in sexp:
            result['text_effects'] = ParserVisitor._get_text_effects(
                cast(SexpNode, sexp['effects'][0]))
        return Property(**result)

    @staticmethod
    def _get_pin(sexp: SexpNode) -> Pin:
        result: Any = {}
        result['type'] = sexp.get(1, '')
        result['style'] = sexp.get(2, '')
        result['pos'] = sexp['at'][0].pos()
        result['angle'] = sexp['at'][0].get(3, 0.0)
        result['hidden'] = 'hide' in sexp.values()[1:]
        result['length'] = sexp['length'][0].get(1, 0.0)
        if 'effects' in sexp['name'][0]:
            result['name'] = (sexp['name'][0].get(1, ''),
                              ParserVisitor._get_text_effects(
                sexp['name'][0]['effects'][0]))
        else:
            result['name'] = (sexp['name'][0].get(1, ''), TextEffects())
        if 'effects' in sexp['number'][0]:
            result['number'] = (sexp['number'][0].get(1, ''),
                                ParserVisitor._get_text_effects(
                sexp['number'][0]['effects'][0]))
        else:
            result['number'] = (sexp['number'][0].get(1, ''), TextEffects())
        return Pin(**result)

    @staticmethod
    def _get_rectangle(sexp: SexpNode) -> Rectangle:
        return Rectangle(
            start_x=sexp['start'][0].get(1, 0.0),
            start_y=sexp['start'][0].get(2, 0.0),
            end_x=sexp['end'][0].get(1, 0.0),
            end_y=sexp['end'][0].get(2, 0.0),
            stroke_definition=ParserVisitor._get_stroke_definition(
                cast(SexpNode, sexp['stroke'][0])),
            fill=get_fill_type(sexp['fill'][0]['type'][0].get(1, ''))
        )

    @staticmethod
    def _get_polyline(sexp: SexpNode) -> Polyline:
        return Polyline(
            points=[(x.get(1, 0.0), x.get(2, 0.0))
                    for x in cast(SexpNode, sexp['pts'][0])['xy']],
            stroke_definition=ParserVisitor._get_stroke_definition(
                cast(SexpNode, sexp['stroke'][0])),
            fill=get_fill_type(sexp['fill'][0]['type'][0].get(1, ''))
        )

    @staticmethod
    def _get_circle(sexp: SexpNode) -> Circle:
        return Circle(
            center=(sexp['center'][0].get(1, 0.0),
                    sexp['center'][0].get(2, 0.0)),
            radius=sexp['radius'][0].get(1, 0.0),
            stroke_definition=ParserVisitor._get_stroke_definition(
                cast(SexpNode, sexp['stroke'][0])),
            fill=get_fill_type(sexp['fill'][0]['type'][0].get(1, ''))
        )

    @staticmethod
    def _get_arc(sexp: SexpNode) -> Arc:
        return Arc(
            start=(sexp['start'][0].get(1, 0.0), sexp['start'][0].get(2, 0.0)),
            mid=(sexp['mid'][0].get(1, 0.0), sexp['mid'][0].get(2, 0.0)),
            end=(sexp['end'][0].get(1, 0.0), sexp['end'][0].get(2, 0.0)),
            stroke_definition=ParserVisitor._get_stroke_definition(
                sexp['stroke'][0]),
            fill=get_fill_type(sexp['fill'][0]['type'][0].get(1, ''))
        )

    @staticmethod
    def _get_library_symbol(sexp: SexpNode) -> LibrarySymbol:
        pins = [ParserVisitor._get_pin(cast(SexpNode, pin))
                for pin in sexp['pin']]
        properties = [ParserVisitor._get_property(cast(SexpNode, prop))
                      for prop in sexp['property']]
        symbols = [ParserVisitor._get_library_symbol(cast(SexpNode, sym))
                   for sym in sexp['symbol']]
        extend = ''
        if 'power' in sexp:
            extend = 'power'
        if 'extends' in sexp:
            extend = sexp['extends'][0].get(1, '')

        graphics: List[GraphicItem] = []
        for graphic in sexp:
            if graphic.get(0, '') == 'rectangle':
                graphics.append(ParserVisitor._get_rectangle(graphic))
            elif graphic.get(0, '') == 'circle':
                graphics.append(ParserVisitor._get_circle(graphic))
            elif graphic.get(0, '') == 'arc':
                graphics.append(ParserVisitor._get_arc(graphic))
            elif graphic.get(0, '') == 'polyline':
                graphics.append(ParserVisitor._get_polyline(graphic))

#        graphics.extend([ParserVisitor._get_rectangle(cast(SexpNode, rect))
#                        for rect in sexp['rectangle']])
#        graphics.extend([ParserVisitor._get_circle(cast(SexpNode, rect))
#                        for rect in sexp['circle']])
#        graphics.extend([ParserVisitor._get_arc(cast(SexpNode, rect))
#                        for rect in sexp['arc']])
#        graphics.extend([ParserVisitor._get_polyline(cast(SexpNode, rect))
#                        for rect in sexp['polyline']])

        return(LibrarySymbol(
            identifier=sexp.get(1, ''),
            extends=extend,
            #mirror=sexp['mirror'][0][0] if len(sexp['mirror']) > 0 else '',
            in_bom='in_bom' in sexp and sexp['in_bom'][0].get(1, '') == "yes",
            on_board='on_board' in sexp and sexp['on_board'][0].get(
                1, '') == 'yes',
            pin_numbers_hide='pin_numbers' in sexp and 'hide' in sexp['pin_numbers'][0].values(
            ),
            pin_names_hide='pin_names' in sexp and 'hide' in sexp['pin_names'][0].values(
            ),
            pin_names_offset=(-1 if not 'pin_names' in sexp or
                              not 'offset' in sexp['pin_names'][0] else
                              sexp['pin_names'][0]['offset'][0].get(1, 0.0)),
            properties=properties,
            pins=pins,
            units=symbols,
            graphics=graphics))

    @staticmethod
    def _get_pcb_stackup_layers(sexp: SexpNode) -> StackUpLayerSettings:
        return(StackUpLayerSettings(
            name=sexp.values()[1],
            number='0',
            type='' if 'type' not in sexp else sexp['type'][0].get(1, ''),
            color='' if 'color' not in sexp else sexp['color'][0].get(1, ''),
            thickness='' if 'thickness' not in sexp else sexp['thickness'][0].get(
                1, ''),
            material='' if 'material' not in sexp else sexp['material'][0].get(
                1, ''),
            epsilon_r='' if 'epsilon_r' not in sexp else sexp['epsilon_r'][0].get(
                1, ''),
            loss_tangent='' if 'loss_tangent' not in sexp else sexp['loss_tangent'][0].get(
                1, ''),
        ))

    @staticmethod
    def _get_pcb_stackup(sexp: SexpNode) -> StackupSettings:
        return(StackupSettings(
            layers=[ParserVisitor._get_pcb_stackup_layers(
                x) for x in sexp['layer']],
            copper_finish=sexp['copper_finish'][0].get(1, ''),
            dielectric_constraints=sexp['dielectric_constraints'][0].get(
                1, ''),
            edge_connector='' if 'edge_connector' not in sexp else
            sexp['edge_connector'][0].get(1, ''),
            castellated_pads='' if 'castellated_pads' not in sexp else
            sexp['castellated_pads'][0].get(1, ''),
            edge_plating='' if 'edge_plating' not in sexp else
            sexp['edge_plating'][0].get(1, '')
        ))

    @staticmethod
    def _get_pcb_plot_settings(sexp: SexpNode) -> PlotSettings:
        return(PlotSettings(
            layerselection=sexp['layerselection'][0].get(1, ''),
            disableapertmacros=sexp['disableapertmacros'][0].get(1, ''),
            usegerberextensions=sexp['usegerberextensions'][0].get(1, ''),
            usegerberattributes=sexp['usegerberattributes'][0].get(1, ''),
            usegerberadvancedattributes=sexp['usegerberadvancedattributes'][0].get(
                1, ''),
            creategerberjobfile=sexp['creategerberjobfile'][0].get(1, ''),
            svguseinch=sexp['svguseinch'][0].get(1, ''),
            svgprecision=sexp['svgprecision'][0].get(1, ''),
            excludeedgelayer=sexp['excludeedgelayer'][0].get(1, ''),
            plotframeref=sexp['plotframeref'][0].get(1, ''),
            viasonmask=sexp['viasonmask'][0].get(1, ''),
            mode=sexp['mode'][0].get(1, ''),
            useauxorigin=sexp['useauxorigin'][0].get(1, ''),
            hpglpennumber=sexp['hpglpennumber'][0].get(1, ''),
            hpglpenspeed=sexp['hpglpenspeed'][0].get(1, ''),
            hpglpendiameter=sexp['hpglpendiameter'][0].get(1, ''),
            dxfpolygonmode=sexp['dxfpolygonmode'][0].get(1, ''),
            dxfimperialunits=sexp['dxfimperialunits'][0].get(1, ''),
            dxfusepcbnewfont=sexp['dxfusepcbnewfont'][0].get(1, ''),
            psnegative=sexp['psnegative'][0].get(1, ''),
            psa4output=sexp['psa4output'][0].get(1, ''),
            plotreference=sexp['plotreference'][0].get(1, ''),
            plotvalue=sexp['plotvalue'][0].get(1, ''),
            plotinvisibletext=sexp['plotinvisibletext'][0].get(1, ''),
            sketchpadsonfab=sexp['sketchpadsonfab'][0].get(1, ''),
            subtractmaskfromsilk=sexp['subtractmaskfromsilk'][0].get(1, ''),
            outputformat=sexp['outputformat'][0].get(1, ''),
            mirror=sexp['mirror'][0].get(1, ''),
            drillshape=sexp['drillshape'][0].get(1, ''),
            scaleselection=sexp['scaleselection'][0].get(1, ''),
            outputdirectory=sexp['outputdirectory'][0].get(1, ''),
        ))

    def start(self) -> None:
        pass

    def end(self) -> None:
        self.consumer.end()

    def node(self, name: str, sexp: SexpNode) -> None:
        #print(f'{name} {sexp}')

        if name == 'version':
            self.version = sexp.get(1, '')

        elif name == 'generator':
            self.generator = sexp.get(1, '')
            self.consumer.start(self.version, self.generator)

        elif name == 'generator':
            self.generator = sexp.get(1, '')
            self.consumer.start(self.version, self.generator)

        elif name == 'paper':
            self.consumer.visitPaper(sexp.get(1, ''))

        elif name == 'uuid':
            self.consumer.visitIdentifier(sexp.get(1, ''))

        elif name == 'title_block':
            values: Dict[str, Any] = {}
            values['title'] = sexp['title'][0].get(1, '')
            if 'date' in sexp:
                values['date'] = sexp['date'][0].get(1, '')
            if 'rev' in sexp:
                values['rev'] = sexp['rev'][0].get(1, '')
            if 'company' in sexp:
                values['company'] = sexp['company'][0].get(1, '')
            comment = {}
            for com in sexp['comment']:
                comment[com.get(1, 0)] = com.get(2, '')
            values['comment'] = comment
            self.consumer.visitTitleBlock(TitleBlock(**values))

        elif name == 'bus':
            self.consumer.visitBus(Bus(
                identifier=sexp['uuid'][0].get(1, ''),
                pts=sexp['pts'][0].pts(),
                stroke_definition=ParserVisitor._get_stroke_definition(
                    sexp['stroke'][0])))

        elif name == 'bus_entry':
            self.consumer.visitBusEntry(BusEntry(
                identifier=sexp['uuid'][0].get(1, ''),
                pos=sexp['at'][0].pos(),
                size=(sexp['size'][0].get(1, 0.0), sexp['size'][0].get(2, 0.0)),
                stroke_definition=ParserVisitor._get_stroke_definition(
                    sexp['stroke'][0])))

        elif name == 'wire':
            self.consumer.visitWire(Wire(
                identifier=sexp['uuid'][0].get(1, ''),
                pts=sexp['pts'][0].pts(),
                stroke_definition=ParserVisitor._get_stroke_definition(
                    sexp['stroke'][0])))

        elif name == 'junction':
            self.consumer.visitJunction(Junction(
                pos=sexp['at'][0].pos(),
                angle=0,
                identifier=sexp['uuid'][0].get(1, ''),
                diameter=sexp['diameter'][0].get(1, 0.0),
                color=ParserVisitor._rgb(sexp)))

        elif name == 'no_connect':
            self.consumer.visitNoConnect(NoConnect(
                pos=sexp['at'][0].pos(),
                angle=0,
                identifier=sexp['uuid'][0].get(1, '')))

        elif name == 'label':
            self.consumer.visitLocalLabel(LocalLabel(
                pos=sexp['at'][0].pos(),
                angle=sexp['at'][0].get(3, 0.0),
                identifier=sexp['uuid'][0].get(1, ''),
                text=sexp.get(1, ''),
                text_effects=self._get_text_effects(
                    sexp['effects'][0])))

        elif name == 'hierarchical_label':
            self.consumer.visitHierarchicalLabel(HierarchicalLabel(
                pos=sexp['at'][0].pos(),
                angle=sexp['at'][0].get(3, 0.0),
                identifier=sexp['uuid'][0].get(1, ''),
                text=sexp.get(1, ''),
                shape=HierarchicalLabelShape.shape(
                    sexp['shape'][0].get(1, '')),
                text_effects=self._get_text_effects(
                    sexp['effects'][0])))

        elif name == 'global_label':
            self.consumer.visitGlobalLabel(GlobalLabel(
                pos=sexp['at'][0].pos(),
                # [0][3][0])) if len(sexp['at'][0]) > 3 else 0,
                angle=sexp['at'][0].get(3, 0.0),
                identifier=sexp['uuid'][0].get(1, ''),
                shape=sexp['shape'][0].get(1, ''),
                text=sexp.get(1, ''),
                autoplaced='fields_autoplaced' in sexp,
                properties=[ParserVisitor._get_property(x)
                            for x in sexp['property']],
                text_effects=self._get_text_effects(sexp['effects'][0])))

        elif name == 'polyline':
            self.consumer.visitGraphicalLine(GraphicalLine(
                identifier=sexp['uuid'][0].get(1, ''),
                pts=sexp['pts'][0].pts(),
                stroke_definition=ParserVisitor._get_stroke_definition(
                    sexp['stroke'][0])))

        elif name == 'text':
            self.consumer.visitGraphicalText(GraphicalText(
                pos=sexp['at'][0].pos(),
                angle=sexp['at'][0].get(3, 0.0),
                identifier=sexp['uuid'][0].get(1, ''),
                text=sexp.get(1, ''),
                text_effects=self._get_text_effects(
                    sexp['effects'][0])))

        elif name == 'symbol':
            pins_ref = [PinRef(number=x.get(1, ''), identifier=x['uuid'][0].get(
                1, '')) for x in sexp['pin']]
            properties = [ParserVisitor._get_property(cast(SexpNode, prop))
                          for prop in sexp['property']]
            self.consumer.visitSymbol(Symbol(
                pos=sexp['at'][0].pos(),
                angle=sexp['at'][0].get(3, 0.0),
                identifier=sexp['uuid'][0].get(1, ''),
                mirror='' if 'mirror' not in sexp else sexp['mirror'][0].get(
                    1, ''),
                library_identifier=sexp['lib_id'][0].get(1, ''),
                unit=sexp['unit'][0].get(1, 1) if 'unit' in sexp else 1,
                in_bom='in_bom' in sexp and sexp['in_bom'][0].get(
                    1, '') == "yes",
                on_board='on_board' in sexp and sexp['on_board'][0].get(
                    1, '') == 'yes',
                on_schema=not 'on_schema' in sexp or not sexp['on_schema'][0].get(
                    1, '') == 'no',
                autoplaced='fields_autoplaced' in sexp,
                properties=properties,
                pins=pins_ref,
                library_symbol=self.libraries[str(sexp['lib_id'][0].get(1, ''))]))

        elif name == 'lib_symbols':
            self.consumer.startLibrarySymbols()
            for symbol in sexp['symbol']:
                lib_symbol = ParserVisitor._get_library_symbol(
                    cast(SexpNode, symbol))
                self.libraries[lib_symbol.identifier] = lib_symbol
                self.consumer.visitLibrarySymbol(lib_symbol)
            self.consumer.endLibrarySymbols()

        elif name == 'sheet':
            pins = [HierarchicalSheetPin(
                pos=pin['at'][0].pos(),
                angle=pin['at'][0].get(3, 0.0),
                identifier=pin['uuid'][0].get(1, ''),
                name=pin.get(1, ''),
                pin_type=pin.get(2, ''),
                text_effects=self._get_text_effects(pin['effects'][0]))
                for pin in sexp['pin']]

            properties = [ParserVisitor._get_property(
                cast(SexpNode, prop)) for prop in sexp['property']]

            self.consumer.visitHierarchicalSheet(HierarchicalSheet(
                pos=sexp['at'][0].pos(),
                angle=sexp['at'][0].get(3, 0.0),
                identifier=sexp['uuid'][0].get(1, ''),
                size=(sexp['size'][0].get(1, 0.0), sexp['size'][0].get(2, 0.0)),
                autoplaced='fields_autoplaced' in sexp,
                stroke_definition=ParserVisitor._get_stroke_definition(
                    sexp['stroke'][0]),
                fill=ParserVisitor._rgb(sexp['fill'][0]),
                pins=pins, properties=properties))

        elif name == 'sheet_instances':
            self.consumer.startSheetInstances()
            for sheet in sexp['path']:
                self.consumer.visitSheetInstance(HierarchicalSheetInstance(
                    path=sheet.get(1, ''),
                    page=sheet['page'][0].get(1, 0)))
            self.consumer.endSheetInstances()

        elif name == 'symbol_instances':
            self.consumer.startSymbolInstances()
            for path in sexp['path']:
                self.consumer.visitSymbolInstance(SymbolInstance(
                    path=path.get(1, ''),
                    reference=path['reference'][0].get(1, ''),
                    unit=path['unit'][0].get(1, 0),
                    value=path['value'][0].get(1, ''),
                    footprint=path['footprint'][0].get(1, ''),
                    identifier=path.get(1, '')))
            self.consumer.endSymbolInstances()

        elif name == 'general':
            items: Dict[str, str] = {}
            for item in sexp:
                items[item.values()[0]] = item.values()[1]
            self.consumer.visitPcbGeneral(PcbGeneral(**items))

        elif name == 'setup':
            self.consumer.visitPcbSetup(PcbSetup(
                stackup_settings=None if 'stackup' not in sexp else
                ParserVisitor._get_pcb_stackup(sexp['stackup'][0]),
                plot_settings=None if 'pcbplotparams' not in sexp else
                ParserVisitor._get_pcb_plot_settings(sexp['pcbplotparams'][0]),
                pad_to_mask_clearance=sexp['pad_to_mask_clearance'][0].get(
                    1, ''),
                solder_mask_min_width='' if 'solder_mask_min_width' not in sexp else
                                      sexp['solder_mask_min_width'][0].get(
                                          1, ''),
                pad_to_paste_clearance='' if 'pad_to_paste_clearance' not in sexp else
                                       sexp['pad_to_paste_clearance'][0].get(
                                           1, ''),
                pad_to_paste_clearance_ratio='' if 'pad_to_paste_clearance_ratio' not in sexp else
                                             sexp['pad_to_paste_clearance_ratio'][0].get(
                                                 1, ''),
                aux_axis_origin=[] if 'aux_axis_origin' not in sexp else
                [float(x) for x in sexp['aux_axis_origin'][0].values()[1:]],
                grid_origin=[] if 'grid_origin' not in sexp else
                [float(x) for x in sexp['grid_origin'][0].values()[1:]],
                copper_finish='' if 'copper_finish' not in sexp else
                              sexp['copper_finish'][0].get(1, ''),
                dielectric_constraints='' if 'dielectric_constraints' not in sexp else
                                       sexp['dielectric_constraints'][0].get(
                                           1, ''),
                edge_connector='' if 'edge_connector' not in sexp else
                               sexp['edge_connector'][0].get(1, ''),
                castellated_pads='' if 'castellated_pads' not in sexp else
                                 sexp['castellated_pads'][0].get(1, ''),
                edge_plating='' if 'edge_plating' not in sexp else
                             sexp['edge_plating'][0].get(1, '')

            ))

        elif name == 'footprint':
            #            footprint: Dict[str, Any] = {}
            #            library: str = ''
            #            locked: str = ''
            #            placed: str = ''
            #            layer: str = ''
            #            tedit: str = ''
            #            tstamp: str = ''
            #            pos: str = ''
            #            angle: str = ''
            #            descr: str = ''
            #            tags: str = ''
            #            property: str = ''
            #            path: str = ''
            #            autoplace_cost90 = ''
            #            autoplace_cost180 = ''
            #            solder_mask_margin: str = ''
            #            solder_paste_margin: str = ''
            #            solder_paste_ratio: str = ''
            #            clearance: str = ''
            #            zone_connect: str = ''
            #            thermal_width: str = ''
            #            thermal_gap: str = ''
            #            ATTRIBUTES: str = ''
            #            GRAPHIC_ITEMS: str = ''
            #            pads: str = ''
            #            ZONES: str = ''
            #            GROUPS: str = ''
            #            MODEL: str = ''
            self.consumer.visitFootprint(Footprint())

        elif name == 'layers':
            self.consumer.startLayers()
            for layer in sexp:
                self.consumer.visitLayer(PcbLayer(
                    ordinal=int(layer.values()[0]),
                    canonical_name=layer.values()[1],
                    type=layer.values()[2],
                    user_name=layer.values()[3] if len(
                        layer.values()) >= 4 else ''
                ))
            self.consumer.endLayers()

        elif name == 'segment':
            self.consumer.visitSegment(TrackSegment(
                start=(sexp['start'][0].get(1, 0.0),
                       sexp['start'][0].get(2, 0.0)),
                end=(sexp['end'][0].get(1, 0.0), sexp['end'][0].get(2, 0.0)),
                width=sexp['width'][0].get(1, 0.0),
                layer=sexp['layer'][0].get(1, ''),
                net=sexp['net'][0].get(1, 0),
                tstamp=sexp['tstamp'][0].get(1, ''),
                locked='locked' in sexp.values()
            ))

        elif name == 'via':
            self.consumer.visitVia(TrackVia(
                at=sexp['at'][0].pos(),
                size=sexp['size'][0].get(1, 0.0),
                drill=sexp['drill'][0].get(1, 0.0),
                layers=sexp['layers'][0].values()[1:],
                net=sexp['net'][0].get(1, 0),
                tstamp=sexp['tstamp'][0].get(1, ''),
                locked='locked' in sexp.values(),
                remove_unused_layers='remove_unused_layers' in sexp.values(),
                keep_end_layers='keep_end_layers' in sexp.values(),
                free='free' in sexp.values(),
            ))

        elif name == 'net':
            self.consumer.visitNet(Net(
                ordinal=int(sexp.values()[1]),
                netname=sexp.values()[2]
            ))

        elif name == 'gr_line':
            self.consumer.visitPcbGraphicalLine(PcbGraphicalLine(
                start=(sexp['start'][0].get(1, 0.0),
                       sexp['start'][0].get(2, 0.0)),
                end=(sexp['end'][0].get(1, 0.0), sexp['end'][0].get(2, 0.0)),
                angle=0 if 'angle' not in sexp else sexp['angle'][0].get(
                    1, 0.0),
                width=sexp['width'][0].get(1, 0.0),
                layer=sexp['layer'][0].get(1, ''),
                tstamp=sexp['tstamp'][0].get(1, ''),
            ))

        else:
            raise ValueError(f'unknown element in sexp: {name}:{sexp}')
