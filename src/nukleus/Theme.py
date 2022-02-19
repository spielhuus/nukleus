from .model import StrokeDefinition, rgb


themes = {'kicad2000': {
    'wire': StrokeDefinition(
        width=0.12, type='solid', color=rgb(0, 150.0 / 255.0, 0, 1)),
    'pin': StrokeDefinition(
        width=0.12, type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
    'no_connect': StrokeDefinition(
        width=0.12, type='solid', color=rgb(0, 0, 132 / 255.0, 1)),
    'component_outline': StrokeDefinition(
        width=0.2, type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
    'component_body': rgb(1, 1, 194 / 255.0, 1),
    },
}
