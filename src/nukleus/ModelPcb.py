"""from __future__ import annotations"""

from dataclasses import dataclass, field
from typing import Dict, List

from .ModelBase import BaseElement
from .Typing import POS_T

class PcbGeneral(BaseElement):
    """The general token define general information about the board. This section is required."""
    values: Dict[str, str] = {}
    """All General parameters.
       most of the parameters are obsolete, to keep consistency all are saved
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.value: dict[str, str] = kwargs

    def __repr__(self) -> str:
        return str(f'PcbGeneral({self.value})')

    def __str__(self) -> str:
        return str(f'PcbGeneral({self.value})')

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, PcbGeneral):
            return False
        return self.value == __o.value


@dataclass(kw_only=True)
class StackUpLayerSettings(BaseElement):
    """The layer token defines the stack up setting
       of a single layer in the board stack up settings."""
    name: str = ''
    """The layer name attribute is either one of the canonical
       copper or technical layer names listed in the table above
       or dielectric ID if it is dielectric layer."""
    number: str = ''
    """The layer number attribute defines the stack order of the layer."""
    type: str = ''
    """The layer type token defines a string that describes the layer."""
    color: str = ''
    """The optional layer color token defines a string that
       describes the layer color. This is only used on solder
       mask and silkscreen layers."""
    thickness: str = ''
    """The optional layer thickness token defines the
       thickness of the layer where appropriate."""
    material: str = ''
    """The optional layer material token defines a string
       that describes the layer material where appropriate."""
    epsilon_r: str = ''
    """The optional layer epsilon_r token defines the
       dielectric constant of the layer material."""
    loss_tangent: str = ''
    """The optional layer loss_tangent token defines
       the dielectric loss tangent of the layer"""


@dataclass(kw_only=True)
class StackupSettings(BaseElement):
    """The optional stackup toke defines the board stack up settings."""
    layers: List[StackUpLayerSettings] = field(default_factory=list)
    """The layer stack up definitions is a list of layer settings for each layer
       required to manufacture a board including the dielectric material between
       the actual layers defined in the board editor."""
    copper_finish: str = ''
    """The optional copper_finish token is a string that defines the
       copper finish used to manufacture the board."""
    dielectric_constraints: str = ''
    """The optional dielectric_contraints token define if the board
       should meet all dielectric requirements."""
    edge_connector: str = ''
    """The optional edge_connector token defines if the board has
       an edge connector and if the edge connector is bevelled."""
    castellated_pads: str = ''
    """The optional castellated_pads token defines if the board
       edges contain castellated pads."""
    edge_plating: str = ''
    """The optional edge_plating token defines if the
       board edges should be plated."""


@dataclass(kw_only=True)
class PlotSettings(BaseElement):
    layerselection: str = ''
    disableapertmacros: str = ''
    usegerberextensions: str = ''
    usegerberattributes: str = ''
    usegerberadvancedattributes: str = ''
    creategerberjobfile: str = ''
    svguseinch: str = ''
    svgprecision: str = ''
    excludeedgelayer: str = ''
    plotframeref: str = ''
    viasonmask: str = ''
    mode: str = ''
    useauxorigin: str = ''
    hpglpennumber: str = ''
    hpglpenspeed: str = ''
    hpglpendiameter: str = ''
    dxfpolygonmode: str = ''
    dxfimperialunits: str = ''
    dxfusepcbnewfont: str = ''
    psnegative: str = ''
    psa4output: str = ''
    plotreference: str = ''
    plotvalue: str = ''
    plotinvisibletext: str = ''
    sketchpadsonfab: str = ''
    subtractmaskfromsilk: str = ''
    outputformat: str = ''
    mirror: str = ''
    drillshape: str = ''
    scaleselection: str = ''
    outputdirectory: str = ''


@dataclass(kw_only=True)
class PcbSetup(BaseElement):
    """
    The general token define general information about the board. This section is required.
    """
    stackup_settings: StackupSettings|None = None
    plot_settings: PlotSettings|None = None
    pad_to_mask_clearance: str = ''
    solder_mask_min_width: str = ''
    pad_to_paste_clearance: str = ''
    pad_to_paste_clearance_ratio: str = ''
    aux_axis_origin: List[float] = field(default_factory=list)
    grid_origin: List[float] = field(default_factory=list)
    copper_finish: str = ''
    dielectric_constraints: str = ''
    edge_connector: str = ''
    castellated_pads: str = ''
    edge_plating: str = ''

@dataclass(kw_only=True)
class PcbLayer(BaseElement):
    """The layers token defines all of the layers used by the board.
       This section is required."""
    ordinal: int = 0
    """	The layer ORDINAL is an integer used to associate the layer stack
        ordering. This is mostly to ensure correct mapping when the number
        of layers is increased in the future."""
    canonical_name: str = ''
    """The CANONICAL_NAME is the layer name defined for internal board use."""
    type: str = ''
    """The layer TYPE defines the type of layer and can be defined as:
        - jumper
        - mixed
        - power
        - signal
        - user"""
    user_name: str = ''
    """The optional USER_NAME attribute defines the custom user name."""


@dataclass(kw_only=True)
class TrackSegment(BaseElement):
    """
    The segment token defines a track segment.
    """
    start: POS_T = (0, 0)
    """The start token defines the coordinates of the beginning of the line."""
    end: POS_T = (0, 0)
    """The end token defines the coordinates of the end of the line."""
    width: float = 0.0
    """The width token defines the line width."""
    layer: str = ''
    """The layer token defines the canonical layer the track segment resides on."""
    locked: bool = False
    """The optional locked token defines if the line cannot be edited."""
    net: int = 0
    """The net token defines by the net ordinal number which net in the net
       section that the segment is part of."""
    tstamp: str = ''
    """The tstamp token defines the unique identifier of the line object."""


@dataclass(kw_only=True)
class TrackVia(BaseElement):
    """
    The via token defines a track via.
    """
    via_type: str = ''
    """The optional type attribute specifies the via type. Valid via types are
    blind and micro. If no type is defined, the via is a through hole type."""
    locked: bool = False
    """The optional locked token defines if the line cannot be edited."""
    at: POS_T = (0, 0)
    """The at token attributes define the coordinates of the center of the via."""
    size: float = 0.0
    """The size token attribute defines the diameter of the via annular ring."""
    drill: float = 0.0
    """The drill token attribute defines the drill diameter of the via."""
    layers: List[str] = field(default_factory=list)
    """The layers token attributes define the canonical layer set the via connects."""
    remove_unused_layers: bool = False
    """The optional remove_unused_layers token."""
    keep_end_layers: bool = False
    """The optional keep_end_layers token."""
    free: bool = False
    """The optional free token indicates that the via is free to be
       moved outside it’s assigned net."""
    net: int = 0
    """The net token attribute defines by net ordinal number which
    net in the net section that the segment is part of."""
    tstamp: str = ''
    """The tstamp token defines the unique identifier of the line object."""


@dataclass(kw_only=True)
class PcbGraphicalLine(BaseElement):
    """The gr_line token defines a graphical line."""
    start: POS_T = (0, 0)
    """The start token defines the coordinates of the beginning of the line."""
    end: POS_T = (0, 0)
    """The end token defines the coordinates of the end of the line."""
    angle: float = 0.0
    """The optional angle token defines the rotational angle of the line."""
    width: float = 0.0
    """The width token defines the line width."""
    layer: str = ''
    """The layer token defines the canonical layer the line resides on."""
    tstamp: str = ''
    """The tstamp token defines the unique identifier of the line object."""


@dataclass(kw_only=True)
class Net(BaseElement):
    """The net token defines a net for the board. This section is required."""
    ordinal: int = 0
    """The oridinal attribute is an integer that defines the net order."""
    netname: str = ''
    """The net name is a string that defines the name of the net."""


@dataclass(kw_only=True)
class Footprint():
    """
    The footprint token defines a footprint.
    """
    library: str = ''
    locked: str = ''
    placed: str = ''
    layer: str = ''
    tedit: str = ''
    tstamp: str = ''
    pos: str = ''
    angle: str = ''
    descr: str = ''
    tags: str = ''
    property: str = ''
    path: str = ''
    autoplace_cost90 = ''
    autoplace_cost180 = ''
    solder_mask_margin: str = ''
    solder_paste_margin: str = ''
    solder_paste_ratio: str = ''
    clearance: str = ''
    zone_connect: str = ''
    thermal_width: str = ''
    thermal_gap: str = ''
    ATTRIBUTES: str = ''
    GRAPHIC_ITEMS: str = ''
    pads: str = ''
    ZONES: str = ''
    GROUPS: str = ''
    MODEL: str = ''
