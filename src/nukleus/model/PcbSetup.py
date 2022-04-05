from __future__ import annotations

from typing import List, cast

from ..SexpParser import SEXP_T


class PlotSettings:
    def __init__(
        self,
        layerselection: str,
        disableapertmacros: str,
        usegerberextensions: str,
        usegerberattributes: str,
        usegerberadvancedattributes: str,
        creategerberjobfile: str,
        svguseinch: str,
        svgprecision: str,
        excludeedgelayer: str,
        plotframeref: str,
        viasonmask: str,
        mode: str,
        useauxorigin: str,
        hpglpennumber: str,
        hpglpenspeed: str,
        hpglpendiameter: str,
        dxfpolygonmode: str,
        dxfimperialunits: str,
        dxfusepcbnewfont: str,
        psnegative: str,
        psa4output: str,
        plotreference: str,
        plotvalue: str,
        plotinvisibletext: str,
        sketchpadsonfab: str,
        subtractmaskfromsilk: str,
        outputformat: str,
        mirror: str,
        drillshape: str,
        scaleselection: str,
        outputdirectory: str,
    ) -> None:

        self.layerselection: str = layerselection
        self.disableapertmacros: str = disableapertmacros
        self.usegerberextensions: str = usegerberextensions
        self.usegerberattributes: str = usegerberattributes
        self.usegerberadvancedattributes: str = usegerberadvancedattributes
        self.creategerberjobfile: str = creategerberjobfile
        self.svguseinch: str = svguseinch
        self.svgprecision: str = svgprecision
        self.excludeedgelayer: str = excludeedgelayer
        self.plotframeref: str = plotframeref
        self.viasonmask: str = viasonmask
        self.mode: str = mode
        self.useauxorigin: str = useauxorigin
        self.hpglpennumber: str = hpglpennumber
        self.hpglpenspeed: str = hpglpenspeed
        self.hpglpendiameter: str = hpglpendiameter
        self.dxfpolygonmode: str = dxfpolygonmode
        self.dxfimperialunits: str = dxfimperialunits
        self.dxfusepcbnewfont: str = dxfusepcbnewfont
        self.psnegative: str = psnegative
        self.psa4output: str = psa4output
        self.plotreference: str = plotreference
        self.plotvalue: str = plotvalue
        self.plotinvisibletext: str = plotinvisibletext
        self.sketchpadsonfab: str = sketchpadsonfab
        self.subtractmaskfromsilk: str = subtractmaskfromsilk
        self.outputformat: str = outputformat
        self.mirror: str = mirror
        self.drillshape: str = drillshape
        self.scaleselection: str = scaleselection
        self.outputdirectory: str = outputdirectory

    @classmethod
    def parse(cls, sexp: SEXP_T) -> PlotSettings:
        """Parse the sexp string to the element.

        :param sexp [str]: the input string.
        """
        _layerselection: str = ""
        _disableapertmacros: str = ""
        _usegerberextensions: str = ""
        _usegerberattributes: str = ""
        _usegerberadvancedattributes: str = ""
        _creategerberjobfile: str = ""
        _svguseinch: str = ""
        _svgprecision: str = ""
        _excludeedgelayer: str = ""
        _plotframeref: str = ""
        _viasonmask: str = ""
        _mode: str = ""
        _useauxorigin: str = ""
        _hpglpennumber: str = ""
        _hpglpenspeed: str = ""
        _hpglpendiameter: str = ""
        _dxfpolygonmode: str = ""
        _dxfimperialunits: str = ""
        _dxfusepcbnewfont: str = ""
        _psnegative: str = ""
        _psa4output: str = ""
        _plotreference: str = ""
        _plotvalue: str = ""
        _plotinvisibletext: str = ""
        _sketchpadsonfab: str = ""
        _subtractmaskfromsilk: str = ""
        _outputformat: str = ""
        _mirror: str = ""
        _drillshape: str = ""
        _scaleselection: str = ""
        _outputdirectory: str = ""

        for token in sexp[1:]:
            if token[0] == "layerselection":
                _layerselection = token[1]
            elif token[0] == "disableapertmacros":
                _disableapertmacros = token[1]
            elif token[0] == "usegerberextensions":
                _usegerberextensions = token[1]
            elif token[0] == "usegerberattributes":
                _usegerberattributes = token[1]
            elif token[0] == "usegerberadvancedattributes":
                _usegerberadvancedattributes = token[1]
            elif token[0] == "creategerberjobfile":
                _creategerberjobfile = token[1]
            elif token[0] == "svguseinch":
                _svguseinch = token[1]
            elif token[0] == "svgprecision":
                _svgprecision = token[1]
            elif token[0] == "excludeedgelayer":
                _excludeedgelayer = token[1]
            elif token[0] == "plotframeref":
                _plotframeref = token[1]
            elif token[0] == "viasonmask":
                _viasonmask = token[1]
            elif token[0] == "mode":
                _mode = token[1]
            elif token[0] == "useauxorigin":
                _useauxorigin = token[1]
            elif token[0] == "hpglpennumber":
                _hpglpennumber = token[1]
            elif token[0] == "hpglpenspeed":
                _hpglpenspeed = token[1]
            elif token[0] == "hpglpendiameter":
                _hpglpendiameter = token[1]
            elif token[0] == "dxfpolygonmode":
                _dxfpolygonmode = token[1]
            elif token[0] == "dxfimperialunits":
                _dxfimperialunits = token[1]
            elif token[0] == "dxfusepcbnewfont":
                _dxfusepcbnewfont = token[1]
            elif token[0] == "psnegative":
                _psnegative = token[1]
            elif token[0] == "psa4output":
                _psa4output = token[1]
            elif token[0] == "plotreference":
                _plotreference = token[1]
            elif token[0] == "plotvalue":
                _plotvalue = token[1]
            elif token[0] == "plotinvisibletext":
                _plotinvisibletext = token[1]
            elif token[0] == "sketchpadsonfab":
                _sketchpadsonfab = token[1]
            elif token[0] == "subtractmaskfromsilk":
                _subtractmaskfromsilk = token[1]
            elif token[0] == "outputformat":
                _outputformat = token[1]
            elif token[0] == "mirror":
                _mirror = token[1]
            elif token[0] == "drillshape":
                _drillshape = token[1]
            elif token[0] == "scaleselection":
                _scaleselection = token[1]
            elif token[0] == "outputdirectory":
                _outputdirectory = token[1]
            else:
                raise ValueError(f"Unexpected item: {token}")

        return PlotSettings( _layerselection,
            _disableapertmacros,
            _usegerberextensions,
            _usegerberattributes,
            _usegerberadvancedattributes,
            _creategerberjobfile,
            _svguseinch,
            _svgprecision,
            _excludeedgelayer,
            _plotframeref,
            _viasonmask,
            _mode,
            _useauxorigin,
            _hpglpennumber,
            _hpglpenspeed,
            _hpglpendiameter,
            _dxfpolygonmode,
            _dxfimperialunits,
            _dxfusepcbnewfont,
            _psnegative,
            _psa4output,
            _plotreference,
            _plotvalue,
            _plotinvisibletext,
            _sketchpadsonfab,
            _subtractmaskfromsilk,
            _outputformat,
            _mirror,
            _drillshape,
            _scaleselection,
            _outputdirectory,
        )

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings = []
        strings.append(f'{"  " * indent}(pcbplotparams')
        if self.layerselection and self.layerselection != '':
            strings.append(f'{"  " * (indent+1)}(layerselection {self.layerselection})')
        if self.disableapertmacros and self.disableapertmacros != '':
            strings.append(f'{"  " * (indent+1)}(disableapertmacros {self.disableapertmacros})')
        if self.usegerberextensions and self.usegerberextensions != '':
            strings.append(f'{"  " * (indent+1)}(usegerberextensions {self.usegerberextensions})')
        if self.usegerberattributes and self.usegerberattributes != '':
            strings.append(f'{"  " * (indent+1)}(usegerberattributes {self.usegerberattributes})')
        if self.usegerberadvancedattributes and self.usegerberadvancedattributes != '':
            strings.append(f'{"  " * (indent+1)}(usegerberadvancedattributes {self.usegerberadvancedattributes})')
        if self.creategerberjobfile and self.creategerberjobfile != '':
            strings.append(f'{"  " * (indent+1)}(creategerberjobfile {self.creategerberjobfile})')
        if self.svguseinch and self.svguseinch != '':
            strings.append(f'{"  " * (indent+1)}(svguseinch {self.svguseinch})')
        if self.svgprecision and self.svgprecision != '':
            strings.append(f'{"  " * (indent+1)}(svgprecision {self.svgprecision})')
        if self.excludeedgelayer and self.excludeedgelayer != '':
            strings.append(f'{"  " * (indent+1)}(excludeedgelayer {self.excludeedgelayer})')
        if self.plotframeref and self.plotframeref != '':
            strings.append(f'{"  " * (indent+1)}(plotframeref {self.plotframeref})')
        if self.viasonmask and self.viasonmask != '':
            strings.append(f'{"  " * (indent+1)}(viasonmask {self.viasonmask})')
        if self.mode and self.mode != '':
            strings.append(f'{"  " * (indent+1)}(mode {self.mode})')
        if self.useauxorigin and self.useauxorigin != '':
            strings.append(f'{"  " * (indent+1)}(useauxorigin {self.useauxorigin})')
        if self.hpglpennumber and self.hpglpennumber != '':
            strings.append(f'{"  " * (indent+1)}(hpglpennumber {self.hpglpennumber})')
        if self.hpglpenspeed and self.hpglpenspeed != '':
            strings.append(f'{"  " * (indent+1)}(hpglpenspeed {self.hpglpenspeed})')
        if self.hpglpendiameter and self.hpglpendiameter != '':
            strings.append(f'{"  " * (indent+1)}(hpglpendiameter {self.hpglpendiameter})')
        if self.dxfpolygonmode and self.dxfpolygonmode != '':
            strings.append(f'{"  " * (indent+1)}(dxfpolygonmode {self.dxfpolygonmode})')
        if self.dxfimperialunits and self.dxfimperialunits != '':
            strings.append(f'{"  " * (indent+1)}(dxfimperialunits {self.dxfimperialunits})')
        if self.dxfusepcbnewfont and self.dxfusepcbnewfont != '':
            strings.append(f'{"  " * (indent+1)}(dxfusepcbnewfont {self.dxfusepcbnewfont})')
        if self.psnegative and self.psnegative != '':
            strings.append(f'{"  " * (indent+1)}(psnegative {self.psnegative})')
        if self.psa4output and self.psa4output != '':
            strings.append(f'{"  " * (indent+1)}(psa4output {self.psa4output})')
        if self.plotreference and self.plotreference != '':
            strings.append(f'{"  " * (indent+1)}(plotreference {self.plotreference})')
        if self.plotvalue and self.plotvalue != '':
            strings.append(f'{"  " * (indent+1)}(plotvalue {self.plotvalue})')
        if self.plotinvisibletext and self.plotinvisibletext != '':
            strings.append(f'{"  " * (indent+1)}(plotinvisibletext {self.plotinvisibletext})')
        if self.sketchpadsonfab and self.sketchpadsonfab != '':
            strings.append(f'{"  " * (indent+1)}(sketchpadsonfab {self.sketchpadsonfab})')
        if self.subtractmaskfromsilk and self.subtractmaskfromsilk != '':
            strings.append(f'{"  " * (indent+1)}(subtractmaskfromsilk {self.subtractmaskfromsilk})')
        if self.outputformat and self.outputformat != '':
            strings.append(f'{"  " * (indent+1)}(outputformat {self.outputformat})')
        if self.mirror and self.mirror != '':
            strings.append(f'{"  " * (indent+1)}(mirror {self.mirror})')
        if self.drillshape and self.drillshape != '':
            strings.append(f'{"  " * (indent+1)}(drillshape {self.drillshape})')
        if self.scaleselection and self.scaleselection != '':
            strings.append(f'{"  " * (indent+1)}(scaleselection {self.scaleselection})')
        if self.outputdirectory and self.outputdirectory != '':
            strings.append(f'{"  " * (indent+1)}(outputdirectory "{self.outputdirectory}")')

        strings.append(f'{"  " * indent})')
        return "\n".join(strings)

class StackUpLayerSettings:
    def __init__(
        self,
        name: str,
        number: int,
        type: str,
        color: str,
        thickness: float,
        material: str,
        epsilon_r: float,
        loss_tangent: float,
    ) -> None:
        self.name = name
        self.number = number
        self.type = type
        self.color = color
        self.thickness = thickness
        self.material = material
        self.epsilon_r = epsilon_r
        self.loss_tangent = loss_tangent

    @classmethod
    def parse(cls, sexp: SEXP_T) -> StackUpLayerSettings:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype General: The StackUpLayerSettings Object.
        """
        _name: str = str(sexp[1])
        _number: int = 0
        _type: str = ""
        _color: str = ""
        _thickness: float = 0.0
        _material: str = ""
        _epsilon_r: float = 0.0
        _loss_tangent: float = 0.0

        for token in sexp[2:]:
            if token[0] == "number":
                _number = int(token[1])
            elif token[0] == "type":
                _type = token[1]
            elif token[0] == "color":
                _color = token[1]
            elif token[0] == "thickness":
                _thickness = float(token[1])
            elif token[0] == "material":
                _material = token[1]
            elif token[0] == "epsilon_r":
                _epsilon_r = float(token[1])
            elif token[0] == "loss_tangent":
                _loss_tangent = float(token[1])
            else:
                raise ValueError(f"Unknown Layer token {token}")

        return StackUpLayerSettings(
            _name,
            _number,
            _type,
            _color,
            _thickness,
            _material,
            _epsilon_r,
            _loss_tangent,
        )

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        string = f'{"  " * indent}(layer "{self.name}" '
        if self.type and self.type != '':
            string += f'(type "{self.type}")'
        if self.color and self.color != '':
            string += f' (color "{self.color}")'
        if self.thickness and self.thickness != 0:
            string += f' (thickness {self.thickness})'
        if self.material and self.material != '':
            string += f' (material "{self.material}")'
        if self.epsilon_r and self.epsilon_r != 0:
            string += f' (epsilon_r {self.epsilon_r})'
        if self.loss_tangent and self.loss_tangent != '':
            string += f' (loss_tangent {self.loss_tangent})'
        string += ')'
        return string

class StackupSettings():
    def __init__(self, layers: List[StackUpLayerSettings], copper_finish: str,
                 dielectric_constraints: str, edge_connector: str,
                 castellated_pads: str , edge_plating: str) -> None:
        self.layers: List[StackUpLayerSettings] = layers
        self.copper_finish: str = copper_finish
        self.dielectric_constraints: str = dielectric_constraints
        self.edge_connector: str = edge_connector
        self.castellated_pads: str = castellated_pads
        self.edge_plating: str = edge_plating

    @classmethod
    def parse(cls, sexp: SEXP_T) -> StackupSettings:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype General: The PcbSetup Object.
        """
        _layers: List[StackUpLayerSettings] = []
        _copper_finish = ''
        _dielectric_constraints = ''
        _edge_connector = ''
        _castellated_pads = ''
        _edge_plating = ''

        for token in sexp[1:]:
            if token[0] == 'layer':
                _layers.append(StackUpLayerSettings.parse(cast(SEXP_T, token)))
            elif token[0] == 'copper_finish':
                _copper_finish = token[1]
            elif token[0] == 'dielectric_constraints':
                _dielectric_constraints = token[1]
            elif token[0] == 'edge_connector':
                _edge_connector = token[1]
            elif token[0] == 'castellated_pads':
                _castellated_pads = token[1]
            elif token[0] == 'edge_plating':
                _edge_plating = token[1]
            else:
                raise ValueError(f"Unknown token {token}")

        return StackupSettings(_layers, _copper_finish, #_LAYER_STACK_UP_DEFINITIONS,
                                    _dielectric_constraints, _edge_connector,
                                    _castellated_pads, _edge_plating)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings = []
        strings.append(f'{"  " * indent}(stackup')
        for layer in self.layers:
            strings.append(layer.sexp(indent+1))
        if self.copper_finish != None and self.copper_finish != '':
            strings.append(f'{"  " * (indent + 1)}(copper_finish "{self.copper_finish}")')
        if self.dielectric_constraints != None and self.dielectric_constraints != '':
            strings.append(f'{"  " * (indent + 1)}(dielectric_constraints {self.dielectric_constraints})')
        if self.edge_connector != None and self.edge_connector != '':
            strings.append(f'{"  " * (indent + 1)}(edge_connector {self.edge_connector})')
        if self.castellated_pads != None and self.castellated_pads != '':
            strings.append(f'{"  " * (indent + 1)}(castellated_pads {self.castellated_pads})')
        if self.edge_plating != None and self.edge_plating != '':
            strings.append(f'{"  " * (indent + 1)}(edge_plating {self.edge_plating})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)

class PcbSetup:
    """
    The general token define general information about the board. This section is required.
    """

    def __init__(self, stackup_settings: StackupSettings|None,
            plot_settings : PlotSettings|None,
            pad_to_mask_clearance: str, solder_mask_min_width: str,
            pad_to_paste_clearance: str, pad_to_paste_clearance_ratio: str,
            aux_axis_origin: List[float], grid_origin: str,  copper_finish: str,
            dielectric_constraints: str, edge_connector: str,
            castellated_pads: str, edge_plating: str) -> None:

        self.stackup_settings: StackupSettings|None = stackup_settings
        self.plot_settings: PlotSettings|None = plot_settings
        self.pad_to_mask_clearance: str = pad_to_mask_clearance
        self.solder_mask_min_width: str = solder_mask_min_width
        self.pad_to_paste_clearance: str = pad_to_paste_clearance
        self.pad_to_paste_clearance_ratio: str = pad_to_paste_clearance_ratio
        self.aux_axis_origin: List[float] = aux_axis_origin
        self.grid_origin: str = grid_origin
        self.copper_finish: str = copper_finish
        self.dielectric_constraints: str = dielectric_constraints
        self.edge_connector: str = edge_connector
        self.castellated_pads: str = castellated_pads
        self.edge_plating: str = edge_plating

    @classmethod
    def parse(cls, sexp: SEXP_T) -> PcbSetup:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype General: The PcbSetup Object.
        """
        _pad_to_mask_clearance = ""
        _solder_mask_min_width = ""
        _pad_to_paste_clearance = ""
        _pad_to_paste_clearance_ratio = ""
        _aux_axis_origin: List[float] = []
        _grid_origin = ""
        _copper_finish = ""
        _dielectric_constraints = ""
        _edge_connector = ""
        _castellated_pads = ""
        _edge_plating = ""
        _plot_settings: PlotSettings|None = None
        _stack_up_settings: StackupSettings|None = None


        for token in sexp[1:]:
            if token[0] == "pad_to_mask_clearance":
                _pad_to_mask_clearance = token[1]
            elif token[0] == "solder_mask_min_width":
                _solder_mask_min_width = token[1]
            elif token[0] == "pad_to_paste_clearance":
                _pad_to_paste_clearance = token[1]
            elif token[0] == "pad_to_paste_clearance_ratio":
                _pad_to_paste_clearance_ratio = token[1]
            elif token[0] == "aux_axis_origin":
                _aux_axis_origin = [float(x) for x in token[1:]]
            elif token[0] == "grid_origin":
                _grid_origin = token[1]
            elif token[0] == "stackup":
                _stack_up_settings = StackupSettings.parse(cast(SEXP_T, token))
            elif token[0] == "pcbplotparams":
                _plot_settings = PlotSettings.parse(cast(SEXP_T, token))

        return PcbSetup(_stack_up_settings, _plot_settings, _pad_to_mask_clearance,
                        _solder_mask_min_width, _pad_to_paste_clearance,
                        _pad_to_paste_clearance_ratio, _aux_axis_origin, _grid_origin,
                        _copper_finish, _dielectric_constraints, _edge_connector,
                        _castellated_pads, _edge_plating)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings = []
        strings.append(f'{"  " * indent}(setup')
        if self.stackup_settings:
            strings.append(self.stackup_settings.sexp(indent+1))

        if self.pad_to_mask_clearance and self.pad_to_mask_clearance != '':
            strings.append(f'{"  " * (indent+1)}(pad_to_mask_clearance {self.pad_to_mask_clearance})')
        if self.solder_mask_min_width and self.solder_mask_min_width != '':
            strings.append(f'{"  " * (indent+1)}(solder_mask_min_width {self.solder_mask_min_width})')
        if self.pad_to_paste_clearance and self.pad_to_paste_clearance != '':
            strings.append(f'{"  " * (indent+1)}(pad_to_paste_clearance {self.pad_to_paste_clearance})')
        if self.pad_to_paste_clearance_ratio and self.pad_to_paste_clearance_ratio != '':
            strings.append(f'{"  " * (indent+1)}(pad_to_paste_clearance_ratio {self.pad_to_paste_clearance_ratio})')
        if self.aux_axis_origin and self.aux_axis_origin != '':
            strings.append(f'{"  " * (indent+1)}(aux_axis_origin {" ".join([str(x) for x in self.aux_axis_origin])})')
        if self.grid_origin and self.grid_origin != '':
            strings.append(f'{"  " * (indent+1)}(grid_origin {" ".join([str(x) for x in self.grid_origin])})')

        if self.plot_settings:
            strings.append(self.plot_settings.sexp(indent+1))
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
