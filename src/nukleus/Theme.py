from .model import Wire, Junction, NoConnect, Symbol, \
    LibrarySymbol, GlobalLabel, LocalLabel, FillType, \
    Pin, Polyline, Rectangle, Justify, \
    StrokeDefinition, TextEffects, rgb


themes = {'kicad2000': {
    'wire': StrokeDefinition(
        0.12, 'solid', rgb(0, 150.0 / 255.0, 0, 1)),
    'pin': StrokeDefinition(
        0.12, 'solid', rgb(132 / 255.0, 0, 0, 1)),
    'no_connect': StrokeDefinition(
        0.12, 'solid', rgb(0, 0, 132 / 255.0, 1)),
    'component_outline': StrokeDefinition(
        0.2, 'solid', rgb(132 / 255.0, 0, 0, 1)),
    'component_body': rgb(1, 1, 194 / 255.0, 1),
    },
}
