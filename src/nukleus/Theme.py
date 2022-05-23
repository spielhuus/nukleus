"""
The Theme for the plotting of the diagrams.
"""
from .ModelBase import TextEffects, Justify, StrokeDefinition, rgb

FONT_THICKNESS=0.0

themes = {'kicad2000': {
    'border': {
        'width': 5.,
        'line': StrokeDefinition(
            width=0.12, stroke_type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
        'comment_1': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'comment_2': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'comment_3': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'comment_4': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'comment_5': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'title': TextEffects(
            face='osifont', font_width=2.54, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'text': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
    },
    'text_effects': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.18, font_style=[],
        justify=[Justify.CENTER], hidden=False
    ),
    'pin_number': TextEffects(
        face='osifont', font_width=0.5, font_height=0.5,
        font_thickness=0.18, font_style=[],
        justify=[Justify.BOTTOM], hidden=False
    ),
    'pin_name': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.25, font_style=[],
        justify=[], hidden=False
    ),
    'netname': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.25, font_style=[],
        justify=[], hidden=False
    ),
    'wire': StrokeDefinition(
        width=0.25, stroke_type='solid', color=rgb(0, 150.0 / 255.0, 0, 1)),
    'pin': StrokeDefinition(
        width=0.25, stroke_type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
    'no_connect': StrokeDefinition(
        width=0.18, stroke_type='solid', color=rgb(0, 0, 132 / 255.0, 1)),
    'component_outline': StrokeDefinition(
        width=0.2, stroke_type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
    'component_body': rgb(1, 1, 194 / 255.0, 1),
    'local_label': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.18, font_style=[],
        justify=[], hidden=False
    ),
    'global_label': {
            'border_color': rgb(0, 0, 0, 1),
            'border_width': 0.1,
            'border_style': 'solid',
            'fill_color': rgb(1, 1, 1, 1),
            'hspacing': 2,
            'vspacing': 0.35
        }
    },
    'notebook': {
    'border': {
        'width': 5.,
        'line': StrokeDefinition(
            width=0.12, stroke_type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
        'comment_1': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'comment_2': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'comment_3': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'comment_4': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'comment_5': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'title': TextEffects(
            face='osifont', font_width=2.54, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
        'text': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False
        ),
    },
    'text_effects': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.18, font_style=[],
        justify=[Justify.CENTER], hidden=False
    ),
    'pin_number': TextEffects(
        face='osifont', font_width=0.5, font_height=0.5,
        font_thickness=0.18, font_style=[],
        justify=[Justify.BOTTOM], hidden=False
    ),
    'pin_name': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.25, font_style=[],
        justify=[], hidden=False
    ),
    'netname': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.25, font_style=[],
        justify=[], hidden=False
    ),
    'wire': StrokeDefinition(
        width=0.25, stroke_type='solid', color=rgb(1, 1, 1, 1)),
    'pin': StrokeDefinition(
        width=0.25, stroke_type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
    'no_connect': StrokeDefinition(
        width=0.18, stroke_type='solid', color=rgb(0, 0, 132 / 255.0, 1)),
    'component_outline': StrokeDefinition(
        width=0.2, stroke_type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
    'component_body': rgb(1, 1, 194 / 255.0, 1),
    'local_label': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.18, font_style=[],
        justify=[], hidden=False
    ),
    'global_label': {
            'border_color': rgb(0, 0, 0, 1),
            'border_width': 0.1,
            'border_style': 'solid',
            'fill_color': rgb(1, 1, 1, 1),
            'hspacing': 2,
            'vspacing': 0.35
        }
    },
    'console': {
    'border': {
        'width': 5.,
        'line': StrokeDefinition(
            width=0.12, stroke_type='solid', color=rgb(132 / 255.0, 0, 0, 1)),
        'comment_1': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False, color=rgb(1, 0, 0, 1)
        ),
        'comment_2': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False, color=rgb(1, 0, 0, 1)
        ),
        'comment_3': TextEffects(
            face='osifont', font_width=2.54, font_height=2.54,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False, color=rgb(1, 0, 0, 1)
        ),
        'comment_4': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False, color=rgb(1, 0, 0, 1)
        ),
        'comment_5': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False, color=rgb(1, 0, 0, 1)
        ),
        'title': TextEffects(
            face='osifont', font_width=2.54, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False, color=rgb(1, 0, 0, 1)
        ),
        'text': TextEffects(
            face='osifont', font_width=1.27, font_height=1.27,
            font_thickness=0.25, font_style=[],
            justify=[Justify.LEFT], hidden=False, color=rgb(1, 0, 0, 1)
        ),
    },
    'text_effects': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.18, font_style=[],
        justify=[Justify.CENTER], hidden=False, color=rgb(.7, .7, .7, 1)
    ),
    'pin_number': TextEffects(
        face='osifont', font_width=0.5, font_height=0.5,
        font_thickness=0.18, font_style=[],
        justify=[Justify.BOTTOM], hidden=False, color=rgb(1, 1, 1, 1)
    ),
    'pin_name': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.25, font_style=[],
        justify=[], hidden=False, color=rgb(1, 1, 1, 1)
    ),
    'netname': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.25, font_style=[],
        justify=[], hidden=False, color=rgb(2, 4, 5, 1)
    ),
    'wire': StrokeDefinition(
        width=0.25, stroke_type='solid', color=rgb(.2, .2, .2, 1)),
    'pin': StrokeDefinition(
        width=0.25, stroke_type='solid', color=rgb(.2, .2, .3, 1)),
    'no_connect': StrokeDefinition(
        width=0.18, stroke_type='solid', color=rgb(0.1, 0.0, 0.2, 1)),
    'component_outline': StrokeDefinition(
        width=0.2, stroke_type='solid', color=rgb(.1, 0.1, 0.2, 1)),
    'component_body': rgb(1, 1, 194 / 255.0, 1),
    'local_label': TextEffects(
        face='osifont', font_width=1.27, font_height=1.27,
        font_thickness=0.18, font_style=[],
        justify=[], hidden=False, color=rgb(1, 1, 1, 1)
    ),
    'global_label': {
            'border_color': rgb(0, 0, 0, 1),
            'border_width': 0.1,
            'border_style': 'solid',
            'fill_color': rgb(1, 1, 1, 1),
            'hspacing': 2,
            'vspacing': 0.35
        }
    },
}
