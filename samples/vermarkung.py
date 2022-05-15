from io import BytesIO

import sys
sys.path.append('src')
sys.path.append('../src')

import nukleus
from nukleus.model.StrokeDefinition import StrokeDefinition
from nukleus.Plot import plot, PlotContext
from nukleus.PlotBase import *

Spacing = 5.08
PanelHeight = 128.5
PCBHeight = 108.1
PCBBottom = 10.08

BORDER_X = 20
BORDER_Y = 20

elements = []
for x in (0,4,8,12,16,20):
    elements.append(DrawLine([(BORDER_X + x*Spacing, BORDER_Y), (BORDER_X + x*Spacing, BORDER_Y + PanelHeight)], 0.35, rgb(0, 0, 0, 1), ''))



for x in range(5):
    elements.append(DrawDimension([(BORDER_X + x * 4 * Spacing, BORDER_Y + PanelHeight), (BORDER_X + (x + 1) * 4 * Spacing, BORDER_Y + PanelHeight)],
        5, 0, 1, "xxxx", 0.18, rgb(1, 0, 0, 1), StrokeDefinition()))

elements.append(DrawLine([(BORDER_X, BORDER_Y), (BORDER_X + 122, BORDER_Y)], 0.35, rgb(0, 0, 0, 1), ''))
elements.append(DrawLine([(BORDER_X, BORDER_Y + PanelHeight), (BORDER_X + 122, BORDER_Y + PanelHeight)], 0.35, rgb(0, 0, 0, 1), ''))
elements.append(DrawLine([(BORDER_X, BORDER_Y + PCBBottom), (BORDER_X + 115, BORDER_Y + PCBBottom)], 0.1, rgb(0, 0, 0, 1), ''))
elements.append(DrawLine([(BORDER_X, BORDER_Y + PCBBottom + PCBHeight), (BORDER_X + 115, BORDER_Y + PCBBottom + PCBHeight)], 0.1, rgb(0, 0, 0, 1), ''))

for x in (2,6,10,14,18):
    elements.append(DrawLine([(BORDER_X + (x * Spacing), BORDER_Y + 15), (BORDER_X + (x * Spacing), BORDER_Y + 120)], 0.1, rgb(0, 0, 0, 1), ''))

for y in (0,4,8,12,16):
    elements.append(DrawLine([(BORDER_X + 3, BORDER_Y + 21.02 + y * Spacing), (BORDER_X + 122, BORDER_Y + 21.82 + y * Spacing)], 0.1, rgb(0, 0, 0, 1), ''))

for x in (2,6,10,14,18):
    for y in (0,4,8,12,16):
        elements.append(DrawCircle(((BORDER_X + x * Spacing), (BORDER_Y + 21.82 + (y * Spacing))), 2.7,  0.1, rgb(0, 0, 0, 1), ''))

x_pos = 1
#horizontal markings top
for name in ('4HP\n20.00', '8HP\n40.3', '12HP\n60.6', '16HP\n80.9', '20HP\n101.3'):
    pos = BORDER_X + (x_pos * 2) * Spacing
    elements.append(DrawText((pos, 10), name, 2, TextEffects(face='osifont', font_width=2, font_height=1.28, hidden=False)))
    x_pos += 2


#% horizontal markings mounting holes
elements.append(DrawLine([(BORDER_X, BORDER_Y + 114), (BORDER_X + 10.16, BORDER_Y + 114)], 0.1, rgb(0, 0, 0, 1), ''))
elements.append(DrawDimension([(30, 30), (100, 100)],
    -10, 0, 1, "xxxx", 0.18, rgb(0, 0, 0, 1), StrokeDefinition()))
#\draw[thin,{Latex[scale=1.5]}-{Latex[scale=1.5]}] (0,114mm) -- (10.16mm,114mm) node[midway,above,align = center]{10.16};
#\draw[thin,{Latex[scale=1.5]}-{Latex[scale=1.5]}] (10.16mm,114mm) -- (30.48mm,114mm) node[near end,above,align = right]{20.32};
#\draw[thin,{Latex[scale=1.5]}-{Latex[scale=1.5]}] (30.48mm,114mm) -- (50.8mm,114mm) node[near end,above,align = right]{20.32};

#vertical markings
#vertical grid
for y in (0, PanelHeight):
    elements.append(DrawLine([(10, BORDER_Y + y), (BORDER_X, BORDER_Y + y)], 0.1, rgb(0, 0, 0, 1), ''))
for y in (PCBBottom, PCBBottom+PCBHeight):
    elements.append(DrawLine([(10, BORDER_Y + y), (BORDER_X, BORDER_Y + y)], 0.1, rgb(0, 0, 0, 1), ''))

elements.append(DrawText((110,PCBBottom), '11.66', 90, TextEffects(face='osifont', font_width=2, font_height=1.28, hidden=False)))
#\draw[thin,{Latex[scale=1.5]}-{Latex[scale=1.5]}] (110mm,\PCBBottom) -- (110mm,\PCBBottom + 11.66mm) node[midway,above,align = center,rotate=90]{11.66};
elements.append(DrawText((110,PCBBottom + PCBHeight - 15.24), '15.24', 0, TextEffects(face='osifont', font_width=2, font_height=1.28, hidden=False)))
#\draw[thin,{Latex[scale=1.5]}-{Latex[scale=1.5]}] (110mm,\PCBBottom + \PCBHeight - 15.24mm) -- (110mm,\PCBBottom + \PCBHeight) node[midway,above,align = center,rotate=90]{15.24};

#\def\last{0}
#\def\widths{{21.82,20.32,20.32,20.32,20.32,25.4}}
#\foreach \y [count=\i from 0)] in {21.82mm,42.14mm,62.46mm,82.78mm,103.1mm,128.5mm} {
#    \draw[thin,{Latex[scale=1.5]}-{Latex[scale=1.5]}] (120mm,\last) -- (120mm,\y) node[midway,above,align = center,rotate=90]{\pgfmathparse{\widths[\i]}\pgfmathresult};
#    \global\let\last=\y
#}

buffer = BytesIO()
with PlotContext('vermarkung.svg', 500, 200, 8, 'svg') as context:
    for e in elements:
        e.draw(context.ctx)

