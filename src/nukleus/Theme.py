from nukleus.model.TextEffects import Justify, TextEffects

from .model import StrokeDefinition, rgb

themes = {'kicad2000': {
    'border': {
        'width': 5.,
        'line': StrokeDefinition(
            width=0.12, type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
        'comment_1': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness='', font_style='',
            justify=[], hidden=False
        ),
        'comment_2': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness='', font_style='',
            justify=[], hidden=False
        ),
        'comment_3': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness='', font_style='',
            justify=[], hidden=False
        ),
        'comment_4': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness='', font_style='',
            justify=[], hidden=False
        ),
        'comment_5': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness='', font_style='',
            justify=[], hidden=False
        ),
    },
    'text_effects': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness='', font_style='',
        justify=[Justify.CENTER], hidden=False
    ),
    'pin_number': TextEffects(
        face='osifont', font_width=0.75, font_height=0.75,
        font_thickness='', font_style='',
        justify=[], hidden=False
    ),
    'pin_name': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness='', font_style='',
        justify=[], hidden=False
    ),
    'wire': StrokeDefinition(
        width=0.12, type='solid', color=rgb(0, 150.0 / 255.0, 0, 1)),
    'pin': StrokeDefinition(
        width=0.12, type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
    'no_connect': StrokeDefinition(
        width=0.12, type='solid', color=rgb(0, 0, 132 / 255.0, 1)),
    'component_outline': StrokeDefinition(
        width=0.2, type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
    'component_body': rgb(1, 1, 194 / 255.0, 1),
    'global_label': {
            'border_color': rgb(0, 0, 0, 1),
            'border_width': 0.1,
            'border_style': 'solid',
            'fill_color': rgb(0.8, 0.8, 0.8, 1),
            'hspacing': 2,
            'vspacing': 0.35
        }
    },
    'notebook': {
    'border': {
        'width': 5.,
        'line': StrokeDefinition(
            width=0.12, type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
        'comment_1': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness='', font_style='',
            justify=[], hidden=False
        ),
        'comment_2': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness='', font_style='',
            justify=[], hidden=False
        ),
        'comment_3': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness='', font_style='',
            justify=[], hidden=False
        ),
        'comment_4': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness='', font_style='',
            justify=[], hidden=False
        ),
        'comment_5': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness='', font_style='',
            justify=[], hidden=False
        ),
    },
    'text_effects': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness='', font_style='',
        justify=[Justify.CENTER], hidden=False
    ),
    'pin_number': TextEffects(
        face='osifont', font_width=0.75, font_height=0.75,
        font_thickness='', font_style='',
        justify=[], hidden=False
    ),
    'pin_name': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness='', font_style='',
        justify=[], hidden=False
    ),
    'wire': StrokeDefinition(
        width=0.25, type='solid', color=rgb(0, 0, 0, 1)),
    'pin': StrokeDefinition(
        width=0.18, type='solid', color=rgb(0, 0, 0, 1)),
    'no_connect': StrokeDefinition(
        width=0.18, type='solid', color=rgb(0, 0, 0, 1)),
    'component_outline': StrokeDefinition(
        width=0.25, type='solid', color=rgb(0, 0, 0, 1)),
    'component_body': rgb(0, 0, 0, 0),
    'global_label': {
            'border_color': rgb(0, 0, 0, 1),
            'border_width': 0.1,
            'border_style': 'solid',
            'fill_color': rgb(0, 0, 0, 1),
            'hspacing': 2,
            'vspacing': 0.35
        }
    },
}
