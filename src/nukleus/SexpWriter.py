from os import wait
from typing import List

import sys

from .AbstractParser import AbstractParser
from .ModelBase import *
from .ModelPcb import *
from .ModelSchema import *

def ffmt(number: float) -> int|float:
    """
    convert float to int when there are no decimal places.

    :param number float: The float
    :rtype int|float: The return number.
    """
    if int(number) == number:
        return int(number)
    return number


class SexpWriter(AbstractParser):
    """Write the schema to the output file"""

    def __init__(self, child: AbstractParser|None = None):
        super().__init__(child)
        self.content: List[str] = []
        self.indent: int = 1

        self.version = ''
        self.identifier = ''
        self.generator = ''
        self.paper = ''

    @staticmethod
    def _stroke_definition(stroke_definition: StrokeDefinition|None, indent: int) -> str:
        string: str = ''
        if stroke_definition:
            string += f'{"  " * indent}(stroke '
            string += f'(width {stroke_definition.width:g}) '
            string += f'(type {stroke_definition.stroke_type}) '
            string += f'(color {ffmt(stroke_definition.color.r)} '
            string += f'{ffmt(stroke_definition.color.g)} '
            string += f'{ffmt(stroke_definition.color.b)} '
            string += f'{ffmt(stroke_definition.color.a)}))'

        return string

    @staticmethod
    def _text_effects(text_effects: TextEffects|None, indent: int) -> str:
        string: str = ''
        if text_effects:
            string += f'{"  " * indent}(effects '
            string += '' if text_effects.face == '' else f'(face {text_effects.face}) '
            string += f'(font (size {text_effects.font_height:g} {text_effects.font_width:g})'
            if text_effects.font_thickness != 0:
                string += f' (thickness {text_effects.font_thickness})'
            for style in text_effects.font_style:
                string += f' {style}'
            string += ')'
            if len(text_effects.justify) > 0:
                string += f' (justify {Justify.string(text_effects.justify)})'
            if text_effects.hidden:
                string += ' hide'
            string += ')'
        return string

    def _property(self, property: Property|None, indent: int):
        if property:
            self.content.append(
                f'{"  " * indent}(property "{property.key}" "{property.value}" '
                f'(id {property.id}) (at {ffmt(property.pos[0])} '
                f'{ffmt(property.pos[1])} {ffmt(property.angle)})'
            )
            if property.text_effects:
                self.content.append(self._text_effects(
                    property.text_effects, indent=indent + 1))
                self.content.append(f'{"  " * indent})')
            else:
                self.content[-1] += ')'

    def _pin(self, pin: Pin|None, indent: int):
        if pin:
            string = f'{"  " * indent}(pin {pin.type} {pin.style} (at {pin.pos[0]:g} '
            string += f'{pin.pos[1]:g} {pin.angle:g}) (length {pin.length:g})'
            if pin.hidden:
                string += ' hide'
            self.content.append(string)
            self.content.append(
                f'{"  " * (indent + 1)}(name "{pin.name[0]}" '
                f'{self._text_effects(pin.name[1], indent=0)})')
            self.content.append(
                f'{"  " * (indent + 1)}(number "{pin.number[0]}" '
                f'{self._text_effects(pin.number[1], indent=0)})')
            self.content.append(f'{"  " * indent})')

    def _graph(self, graph: GraphicItem, indent: int):
        if isinstance(graph, Polyline):
            self.content.append(f'{"  " * indent}(polyline')
            self.content.append(f'{"  " * (indent + 1)}(pts')
            for _pts in graph.points:
                self.content.append(f'{"  " * (indent + 2)}(xy {ffmt(_pts[0])} {ffmt(_pts[1])})')
            self.content.append(f'{"  " * (indent + 1)})')
            self.content.append(self._stroke_definition(graph.stroke_definition, indent=indent+1))
            self.content.append(
                f'{"  " * (indent + 1)}(fill (type {get_fill_str(graph.fill)}))')
            self.content.append(f'{"  " * indent})')

        elif isinstance(graph, Rectangle):
            self.content.append(f'{"  " * indent}(rectangle (start '
                           f'{graph.start_x:g} {graph.start_y:g})'
                           f' (end {graph.end_x:g} {graph.end_y:g})')
            self.content.append(self._stroke_definition(graph.stroke_definition, indent=indent+1))
            self.content.append(
                f'{"  " * (indent + 1)}(fill (type {get_fill_str(graph.fill)}))')
            self.content.append(f'{"  " * indent})')

        elif isinstance(graph, Circle):
            self.content.append(f'{"  " * indent}(circle '
                                f'(center {ffmt(graph.center[0])} {ffmt(graph.center[1])}) '
                                f'(radius {ffmt(graph.radius)})')
            self.content.append(self._stroke_definition(graph.stroke_definition, indent=indent+1))
            self.content.append(
                f'{"  " * (indent + 1)}(fill (type {get_fill_str(graph.fill)}))')
            self.content.append(f'{"  " * indent})')

        elif isinstance(graph, Arc):
            self.content.append(f'{"  " * indent}(arc '
                                f'(start {ffmt(graph.start[0])} {ffmt(graph.start[1])}) '
                                f'(mid {ffmt(graph.mid[0])} {ffmt(graph.mid[1])}) '
                                f'(end {ffmt(graph.end[0])} {ffmt(graph.end[1])})')
            self.content.append(self._stroke_definition(graph.stroke_definition, indent=indent+1))
            self.content.append(
                f'{"  " * (indent + 1)}(fill (type {get_fill_str(graph.fill)}))')
            self.content.append(f'{"  " * indent})')

        elif isinstance(graph, Text):
            self.content.append(f'{"  " * indent}(text "{graph.text} '
                                f' (at {ffmt(graph.pos[0])} {ffmt(graph.pos[1])} {ffmt(graph.angle)})')
            self.content.append(self._text_effects(graph.text_effects, indent=indent+1))
            self.content.append(f'{"  " * indent})')

    def __str__(self) -> str:
        return '\n'.join(self.content)

    def end(self):
        self.content.append(')')
        super().end()

    def startSheetInstances(self):
        self.content.append(f'{"  " * self.indent}(sheet_instances')
        self.indent += 1
        super().startSheetInstances()

    def endSheetInstances(self):
        self.indent -= 1
        self.content.append(f'{"  " * self.indent})')
        super().endSheetInstances()

    def startSymbolInstances(self):
        self.content.append(f'{"  " * self.indent}(symbol_instances')
        self.indent += 1
        super().startSymbolInstances()

    def endSymbolInstances(self):
        self.indent -= 1
        self.content.append(f'{"  " * self.indent})')
        super().endSymbolInstances()

    def start(self, version: str, identifier: str, generator: str,
              paper: str, title_block: TitleBlock):
        self.content.append(
            f"(kicad_sch (version {version}) (generator {generator})")
        self.content.append('')
        self.content.append(f"  (uuid {identifier})")
        self.content.append('')
        self.content.append(f"  (paper \"{paper}\")")
        self.content.append('')
        if title_block:
            self.content.append("  (title_block")
            self.content.append(f"    (title \"{title_block.title}\")")
            self.content.append(f"    (date \"{title_block.date}\")")
            self.content.append(f"    (rev \"{title_block.rev}\")")
            if title_block.company != '':
                self.content.append(f"    (company \"{title_block.company}\")")
            for com in sorted(title_block.comment.keys()):
                self.content.append(f"    (comment {com} \"{title_block.comment[com]}\")")
            self.content.append("  )")
        self.content.append("")
        super().start(version, identifier, generator, paper, title_block)

    def visitWire(self, wire: Wire):
        string = ''
        string += f'{"  " * self.indent}(wire (pts'
        for _pt in wire.pts:
            string += f' (xy {_pt[0]:g} {_pt[1]:g})'
        string += ')'
        self.content.append(string)
        self.content.append(self._stroke_definition(wire.stroke_definition, indent=self.indent+1))
        self.content.append(f'{"  " * (self.indent+1)}(uuid {wire.identifier})')
        self.content.append(f'{"  " * self.indent})')
        super().visitWire(wire)

    def visitJunction(self, junction: Junction):
        self.content.append(f'{"  " * self.indent}(junction (at '
                       f'{junction.pos[0]:g} {junction.pos[1]:g}) '
                       f'(diameter {junction.diameter:g}) '
                       f'(color {ffmt(junction.color.r)} {ffmt(junction.color.g)} '
                       f'{ffmt(junction.color.b)} {ffmt(junction.color.a)})')
        self.content.append(f'{"  " * (self.indent + 1)}(uuid {junction.identifier})')
        self.content.append(f'{"  " * self.indent})')
        super().visitJunction(junction)

    def visitNoConnect(self, no_connect: NoConnect):
        self.content.append(f'{"  " * self.indent}'
               f'(no_connect (at {no_connect.pos[0]} {no_connect.pos[1]}) '
               f'(uuid {no_connect.identifier}))')
        super().visitNoConnect(no_connect)

    def visitLocalLabel(self, local_label: LocalLabel):
        self.content.append(
            f'{"  " * self.indent}(label "{local_label.text}" '
            f'(at {local_label.pos[0]:g} {ffmt(local_label.pos[1])} {ffmt(local_label.angle)})')
        self.content.append(self._text_effects(local_label.text_effects, indent=self.indent+1))
        self.content.append(f'{"  " * (self.indent + 1)}(uuid {local_label.identifier})')
        self.content.append(f'{"  " * self.indent})')
        super().visitLocalLabel(local_label)

    def visitGlobalLabel(self, global_label: GlobalLabel):
        self.content.append(
            f'{"  " * self.indent}(global_label "{global_label.text}" '
                f'(shape {global_label.shape}) '
                f'(at {ffmt(global_label.pos[0])} '
                f'{ffmt(global_label.pos[1])} '
                f'{ffmt(global_label.angle)})'
            f'{"" if not global_label.autoplaced else " (fields_autoplaced)"}'
        )
        self.content.append(self._text_effects(global_label.text_effects, indent=self.indent + 1))
        self.content.append(f'{"  " * (self.indent + 1)}(uuid {global_label.identifier})')
        for prop in global_label.properties:
            self._property(prop, indent=self.indent + 1)
        self.content.append(f'{"  " * self.indent})')
        super().visitGlobalLabel(global_label)

    def visitGraphicalLine(self, graphical_line: GraphicalLine):
        string = ''
        string += f'{"  " * self.indent}(polyline (pts'
        for _pt in graphical_line.pts:
            string += f' (xy {_pt[0]:g} {_pt[1]:g})'
        string += ')'
        self.content.append(string)
        self.content.append(self._stroke_definition(
            graphical_line.stroke_definition, indent=self.indent+1))
        self.content.append(f'{"  " * (self.indent+1)}(uuid {graphical_line.identifier})')
        self.content.append(f'{"  " * self.indent})')
        super().visitGraphicalLine(graphical_line)

    def visitGraphicalText(self, graphical_text: GraphicalText):
        self.content.append( f'{"  " * self.indent}(text "{graphical_text.text}" '
                             f'(at {ffmt(graphical_text.pos[0])} '
                             f'{ffmt(graphical_text.pos[1])} {ffmt(graphical_text.angle)})')
        self.content.append(self._text_effects(graphical_text.text_effects, indent=self.indent+1))
        self.content.append(f'{"  " * (self.indent+1)}(uuid {graphical_text.identifier})')
        self.content.append(f'{"  " * self.indent})')
        super().visitGraphicalText(graphical_text)

    def visitHierarchicalSheet(self, hierarchical_sheet: HierarchicalSheet):
        self.content.append(f'{"  " * self.indent}(sheet (at {hierarchical_sheet.pos[0]} '
                       f'{hierarchical_sheet.pos[1]}) '
                       f'(size {hierarchical_sheet.size[0]} '
                       f'{hierarchical_sheet.size[1]})')
        self.content.append(self._stroke_definition(
            hierarchical_sheet.stroke_definition, indent=self.indent+1))
        self.content.append(f'{"  " * (self.indent + 1)}'
                            f'(fill (color {ffmt(hierarchical_sheet.fill.r)} '
                            f'{ffmt(hierarchical_sheet.fill.g)} '
                            f'{ffmt(hierarchical_sheet.fill.b)} '
                            f'{ffmt(hierarchical_sheet.fill.a)}))')
        self.content.append(f'{"  " * (self.indent + 1)}(uuid {hierarchical_sheet.identifier})')
        for prop in hierarchical_sheet.properties:
            self._property(prop, indent=self.indent+1)
        for pin in hierarchical_sheet.pins:
            self._pin(pin, indent=self.indent+1)
        self.content.append(f'{"  " * self.indent})')
        super().visitHierarchicalSheet(hierarchical_sheet)

    def visitSymbol(self, symbol: Symbol):
        sexp_symbol = f'{"  " * self.indent}(symbol (lib_id "{symbol.library_identifier}")'
        sexp_symbol += f' (at {ffmt(symbol.pos[0])} {ffmt(symbol.pos[1])} {ffmt(symbol.angle)})'
        sexp_symbol += '' if symbol.mirror == '' else f' (mirror {symbol.mirror})'
        sexp_symbol += '' if symbol.unit == 0 else f' (unit {symbol.unit})'
        self.content.append(sexp_symbol)
        sexp_symbol = f'{"  " * (self.indent + 1)}(in_bom {"yes" if symbol.in_bom else "no"}) '
        sexp_symbol += f'(on_board {"yes" if symbol.on_board else "no"})'
        sexp_symbol += ' (fields_autoplaced)' if symbol.autoplaced else ''
        self.content.append(sexp_symbol)
        self.content.append(f'{"  " * (self.indent + 1)}(uuid {symbol.identifier})')
        for prop in symbol.properties:
            self._property(prop, indent=self.indent+1)

        for pin in symbol.pins:
            self.content.append(f'{"  " * (self.indent + 1)}'
                f'(pin "{pin.number}" (uuid {pin.identifier}))')

        self.content.append(f'{"  " * self.indent})')
        super().visitSymbol(symbol)

    def startLibrarySymbols(self):
        self.content.append("  (lib_symbols")
        self.indent += 1
        super().startLibrarySymbols()

    def endLibrarySymbols(self):
        self.indent -= 1
        self.content.append('  )')
        super().endLibrarySymbols()

    def _subsymbol(self, symbol: LibrarySymbol, indent: int):
        sexp_symbol = f'{"  " * indent}(symbol "{symbol.identifier}"'
        self.content.append(sexp_symbol)
        for prop in symbol.properties:
            self._property(prop, indent=indent+1)

        for graphic in symbol.graphics:
            self._graph(graphic, indent=indent+1)

        for pin in symbol.pins:
            self._pin(pin, indent=indent+1)

        self.content.append(f'{"  " * indent})')

    def visitLibrarySymbol(self, symbol: LibrarySymbol):
        sexp_symbol = f'{"  " * self.indent}(symbol "{symbol.identifier}"'
        if symbol.extends != '':
            sexp_symbol += f' ({symbol.extends})'
        if symbol.pin_numbers_hide:
            sexp_symbol += ' (pin_numbers hide)'
        if symbol.pin_names_offset != -1:
            sexp_symbol += f' (pin_names (offset {symbol.pin_names_offset:g})'
            if symbol.pin_names_hide:
                sexp_symbol += ' hide'
            sexp_symbol += ')'
        sexp_symbol += f' (in_bom {"yes" if symbol.in_bom else "no"}) '
        sexp_symbol += f'(on_board {"yes" if symbol.on_board else "no"})'
        self.content.append(sexp_symbol)
        for prop in symbol.properties:
            self._property(prop, indent=self.indent+1)

        for graphic in symbol.graphics:
            self._graph(graphic, indent=self.indent+1)

        for pin in symbol.pins:
            self._pin(pin, indent=self.indent+1)

        for uit in symbol.units:
            self._subsymbol(uit, indent=self.indent+1)

        self.content.append(f'{"  " * self.indent})')
        super().visitLibrarySymbol(symbol)

    def visitSheetInstance(self, sheet: HierarchicalSheetInstance):
        self.content.append(f'{"  " * self.indent}(path "{sheet.path}" (page "{sheet.page}"))')
        super().visitSheetInstance(sheet)

    def visitSymbolInstance(self, symbol: SymbolInstance):
        self.content.append(f'{"  " * self.indent}(path "{symbol.path}"')
        self.content.append(f'{"  " * (self.indent + 1)}'
                            f'(reference "{symbol.reference}") (unit {symbol.unit}) '
                       f'(value "{symbol.value}") (footprint "{symbol.footprint}")')
        self.content.append(f'{"  " * self.indent})')
        super().visitSymbolInstance(symbol)



    def visitPcbGeneral(self, general: PcbGeneral):
        """General Instance"""
        self.content.append(f'{"  " * self.indent}(general ')
        for key, value in general.values.items():
            self.content.append(f'{"  " * (self.indent+1)}({key} {value})')
        self.content.append(f'{"  " * self.indent})')
        super().visitPcbGeneral(general)


    def _stackup_layer_settings(self, stackup_layer_settings: StackUpLayerSettings):
        pass # TODO

    def visitPcbSetup(self, setup: PcbSetup):
        self.content.append(f'{"  " * (self.indent)}(setup ')
        if setup.stackup_settings:
            pass #TODO StackupSettings|None = None
        self.content.append(f'{"  " * (self.indent+1)}'
                            f'(pad_to_mask_clearance {setup.pad_to_mask_clearance})')
        if setup.solder_mask_min_width != '':
            self.content.append(f'{"  " * (self.indent+1)}'
                                f'(solder_mask_min_width {setup.solder_mask_min_width})')
        if setup.pad_to_paste_clearance != '':
            self.content.append(f'{"  " * (self.indent+1)}'
                                f'(pad_to_paste_clearance {setup.pad_to_paste_clearance})')
        if setup.pad_to_paste_clearance_ratio != '':
            self.content.append(f'{"  " * (self.indent+1)}'
                                f'(pad_to_paste_clearance_ratio {setup.pad_to_paste_clearance_ratio})')
        if len(setup.aux_axis_origin) > 0:
            self.content.append(f'{"  " * (self.indent+1)}'
                                f'(aux_axis_origin {setup.aux_axis_origin[0]} {setup.aux_axis_origin[1]})')
        if len(setup.grid_origin) > 0:
            self.content.append(f'{"  " * (self.indent+1)}'
                                f'(grid_origin {setup.grid_origin[0]} {setup.grid_origin[1]})')

        if setup.plot_settings:
            self.content.append(f'{"  " * (self.indent+1)}(pcbplotparams')
            if setup.plot_settings.layerselection != '':
                self.content.append(f'{"  " * (self.indent+2)}'
                                    f'(layerselection {setup.plot_settings.layerselection})')
            if setup.plot_settings.disableapertmacros != '':
                self.content.append(f'{"  " * (self.indent+2)}'
                                    f'(disableapertmacros {setup.plot_settings.disableapertmacros})')
            if setup.plot_settings.usegerberextensions != '':
                self.content.append(f'{"  " * (self.indent+2)}(usegerberextensions {setup.plot_settings.usegerberextensions})')
            if setup.plot_settings.usegerberattributes != '':
                self.content.append(f'{"  " * (self.indent+2)}(usegerberattributes {setup.plot_settings.usegerberattributes})')
            if setup.plot_settings.usegerberadvancedattributes != '':
                self.content.append(f'{"  " * (self.indent+2)}(usegerberadvancedattributes {setup.plot_settings.usegerberadvancedattributes})')
            if setup.plot_settings.creategerberjobfile != '':
                self.content.append(f'{"  " * (self.indent+2)}(creategerberjobfile {setup.plot_settings.creategerberjobfile})')
            if setup.plot_settings.svguseinch != '':
                self.content.append(f'{"  " * (self.indent+2)}(svguseinch {setup.plot_settings.svguseinch})')
            if setup.plot_settings.svgprecision != '':
                self.content.append(f'{"  " * (self.indent+2)}(svgprecision {setup.plot_settings.svgprecision})')
            if setup.plot_settings.excludeedgelayer != '':
                self.content.append(f'{"  " * (self.indent+2)}(excludeedgelayer {setup.plot_settings.excludeedgelayer})')
            if setup.plot_settings.plotframeref != '':
                self.content.append(f'{"  " * (self.indent+2)}(plotframeref {setup.plot_settings.plotframeref})')
            if setup.plot_settings.viasonmask != '':
                self.content.append(f'{"  " * (self.indent+2)}(viasonmask {setup.plot_settings.viasonmask})')
            if setup.plot_settings.mode != '':
                self.content.append(f'{"  " * (self.indent+2)}(mode {setup.plot_settings.mode})')
            if setup.plot_settings.useauxorigin != '':
                self.content.append(f'{"  " * (self.indent+2)}(useauxorigin {setup.plot_settings.useauxorigin})')
            if setup.plot_settings.hpglpennumber != '':
                self.content.append(f'{"  " * (self.indent+2)}(hpglpennumber {setup.plot_settings.hpglpennumber})')
            if setup.plot_settings.hpglpenspeed != '':
                self.content.append(f'{"  " * (self.indent+2)}(hpglpenspeed {setup.plot_settings.hpglpenspeed})')
            if setup.plot_settings.hpglpendiameter != '':
                self.content.append(f'{"  " * (self.indent+2)}(hpglpendiameter {setup.plot_settings.hpglpendiameter})')
            if setup.plot_settings.dxfpolygonmode != '':
                self.content.append(f'{"  " * (self.indent+2)}(dxfpolygonmode {setup.plot_settings.dxfpolygonmode})')
            if setup.plot_settings.dxfimperialunits != '':
                self.content.append(f'{"  " * (self.indent+2)}(dxfimperialunits {setup.plot_settings.dxfimperialunits})')
            if setup.plot_settings.dxfusepcbnewfont != '':
                self.content.append(f'{"  " * (self.indent+2)}(dxfusepcbnewfont {setup.plot_settings.dxfusepcbnewfont})')
            if setup.plot_settings.psnegative != '':
                self.content.append(f'{"  " * (self.indent+2)}(psnegative {setup.plot_settings.psnegative})')
            if setup.plot_settings.psa4output != '':
                self.content.append(f'{"  " * (self.indent+2)}(psa4output {setup.plot_settings.psa4output})')
            if setup.plot_settings.plotreference != '':
                self.content.append(f'{"  " * (self.indent+2)}(plotreference {setup.plot_settings.plotreference})')
            if setup.plot_settings.plotvalue != '':
                self.content.append(f'{"  " * (self.indent+2)}(plotvalue {setup.plot_settings.plotvalue})')
            if setup.plot_settings.plotinvisibletext != '':
                self.content.append(f'{"  " * (self.indent+2)}(plotinvisibletext {setup.plot_settings.plotinvisibletext})')
            if setup.plot_settings.sketchpadsonfab != '':
                self.content.append(f'{"  " * (self.indent+2)}(sketchpadsonfab {setup.plot_settings.sketchpadsonfab})')
            if setup.plot_settings.subtractmaskfromsilk != '':
                self.content.append(f'{"  " * (self.indent+2)}(subtractmaskfromsilk {setup.plot_settings.subtractmaskfromsilk})')
            if setup.plot_settings.outputformat != '':
                self.content.append(f'{"  " * (self.indent+2)}(outputformat {setup.plot_settings.outputformat})')
            if setup.plot_settings.mirror != '':
                self.content.append(f'{"  " * (self.indent+2)}(mirror {setup.plot_settings.mirror})')
            if setup.plot_settings.drillshape != '':
                self.content.append(f'{"  " * (self.indent+2)}(drillshape {setup.plot_settings.drillshape})')
            if setup.plot_settings.scaleselection != '':
                self.content.append(f'{"  " * (self.indent+2)}(scaleselection {setup.plot_settings.scaleselection})')
            if setup.plot_settings.outputdirectory != '':
                self.content.append(f'{"  " * (self.indent+2)}(outputdirectory {setup.plot_settings.outputdirectory})')
            self.content.append(f'{"  " * (self.indent+1)})')
        super().visitPcbSetup(setup)

    def visitFootprint(self, footprint: Footprint):
        """Footprint Instance"""
        super().visitFootprint(footprint)

    def startLayers(self):
        self.content.append(f'{"  " * self.indent}(layers ')
        super().startLayers()

    def endLayers(self):
        self.content.append(f'{"  " * self.indent})')
        super().endLayers()

    def visitLayer(self, layer: PcbLayer):
        username = ')' if layer.user_name == '' else f'"{layer.user_name})'
        self.content.append(f'{"  " * (self.indent+1)}({layer.ordinal} '
                            f'"{layer.canonical_name}" '
                            f'{layer.type} {username}')
        super().visitLayer(layer)

    def visitSegment(self, segment: TrackSegment):
        self.content.append(f'{"  " * (self.indent+1)}(segment '
                            f'(start {segment.start[0]} {segment.start[1]}) '
                            f'(start {segment.end[0]} {segment.end[1]}) '
                            f'(width {segment.width}) '
                            f'(layer "{segment.layer}") '
                            f'{"locked " if segment.locked else ""}'
                            f'(net {segment.net}) '
                            f'(tstamp {segment.tstamp}))')
        super().visitSegment(segment)

    def visitVia(self, via: TrackVia):
        layers = ''
        for layer in via.layers:
            layers += f'" {layer}"'
        self.content.append(f'{"  " * (self.indent+1)}(via '
                            f'(at {via.at[0]} {via.at[1]}) '
                            f'(size {via.size}) '
                            f'(drill {via.drill}) '
                            f'(net {via.net}) '
                            f'(tstamp {via.tstamp}) ')
        super().visitVia(via)

#TODO
#    via_type: str = ''
#    locked: bool = False
#    at: POS_T = (0, 0)
#    size: float = 0.0
#    drill: float = 0.0
#    layers: List[str] = field(default_factory=list)
#    remove_unused_layers: bool = False
#    keep_end_layers: bool = False
#    free: bool = False
#    net: int = 0
#    tstamp: str = ''

    def visitNet(self, net: Net):
        self.content.append(f'{"  " * (self.indent+1)}(net '
                            f'{net.ordinal} '
                            f'"{net.netname}")')
        super().visitNet(net)

    def visitPcbGraphicalLine(self, graphical_line: PcbGraphicalLine):
        self.content.append(f'{"  " * (self.indent+1)}(gr_line '
                            f'(start {graphical_line.start[0]} {graphical_line.start[1]}) '
                            f'(end {graphical_line.end[0]} {graphical_line.end[1]}) '
                            f'(layer "{graphical_line.layer}") '
                            f'(tstamp "{graphical_line.tstamp})')
        super().visitPcbGraphicalLine(graphical_line)
