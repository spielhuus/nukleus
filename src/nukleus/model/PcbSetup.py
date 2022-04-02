from __future__ import annotations

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

    def parse(self, sexp: SEXP_T) -> PlotSettings:
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
                _hpglpendiameter = token[1]
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


class StackUpLayerSettings:
    def __init__(
        self,
        name: str,
        number: int,
        type: str,
        color: str,
        thickness: float,
        material: str,
        epsilon_r: str,
        loss_tangent: str,
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
        _name: str = ""
        _number: int = 0
        _type: str = ""
        _color: str = ""
        _thickness: float = 0.0
        _material: str = ""
        _epsilon_r: str = ""
        _loss_tangent: str = ""

        for token in sexp[1:]:
            if token[0] == "name":
                _name = token[1]
            elif token[0] == "number":
                _number = int(token[1])
            elif token[0] == "type":
                _type = token[1]
            elif token[1] == "color":
                _color = token[1]
            elif token[0] == "thickness":
                _thickness = float(token[1])
            elif token[0] == "material":
                _material = token[1]
            elif token[0] == "epsilon_r":
                _epsilon_r = token[1]
            elif token[0] == "loss_tangent":
                _loss_tangent = token[1]
            else:
                raise ValueError(f"Unknown token {token}")

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
        strings = []
        strings.append(f'{"  " * indent}(setup')
        for key, value in self.values.items():
            strings.append(f'{"  " * (indent + 1)}(%s %s)' % (key, " ".join(value)))
        strings.append(f'{"  " * (indent + 1)}(pcbplotparams')
        for key, value in self.pcb_params.items():
            strings.append(f'{"  " * (indent + 2)}(%s %s)' % (key, value))
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)

class StackupSettings():
    def __init__(self, copper_finish: str, dielectric_constraints: str, edge_connector: str, castellated_pads: str , edge_plating: str) -> None:
        #self.LAYER_STACK_UP_DEFINITIONS: str = #LAYER_STACK_UP_DEFINITIONS
        self.copper_finish: str = copper_finish
        self.dielectric_constraints: str = dielectric_constraints
        self.edge_connector: str = edge_connector
        self.castellated_pads: str = castellated_pads
        self.edge_plating: str = edge_plating




#LAYER_STACK_UP_DEFINITIONS
copper_finish
dielectric_constraints yes |
edge_connector yes |
castellated_pads
edge_plating














class PcbSetup:
    """
    The general token define general information about the board. This section is required.
    """

    def __init__(self, pcb_params, **kwargs) -> None:
        self.pad_to_mask_clearance = kwargs.get("pad_to_mask_clearance", "")
        self.solder_mask_min_width = kwargs.get("solder_mask_min_width", "")
        self.pad_to_paste_clearance = kwargs.get("pad_to_paste_clearance", "")
        self.pad_to_paste_clearance_ratio = kwargs.get(
            "pad_to_paste_clearance_ratio", ""
        )
        self.aux_axis_origin = kwargs.get("aux_axis_origin", "")
        self.grid_origin = kwargs.get("grid_origin", "")
        self.stack_up_settings = []
        self.plot_settings = []

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
        _aux_axis_origin = ""
        _grid_origin = ""

        _copper_finish = ""
        _dielectric_constraints = ""
        _edge_connector = ""
        _castellated_pads = ""
        _edge_plating = ""

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
                _aux_axis_origin = token[1]
            elif token[0] == "grid_origin":
                _grid_origin = token[1]

            elif token[0] == "layers":
                _stack_up_settings = StackUpLayerSettings.parse(token)

        return PcbSetup(_value, _pcb_params)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings = []
        strings.append(f'{"  " * indent}(setup')
        for key, value in self.values.items():
            strings.append(f'{"  " * (indent + 1)}(%s %s)' % (key, " ".join(value)))
        strings.append(f'{"  " * (indent + 1)}(pcbplotparams')
        for key, value in self.pcb_params.items():
            strings.append(f'{"  " * (indent + 2)}(%s %s)' % (key, value))
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
