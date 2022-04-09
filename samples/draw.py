import sys

import matplotlib.pyplot as plt
import logging

sys.path.append('src')
sys.path.append('../src')

import nukleus
from nukleus.draw import Draw, Dot, Label, Line, Element
from nukleus import Circuit
from nukleus.Plot import plot
from nukleus.model.Utils import get_pins
from nukleus.Netlist import Netlist

# initialize the logger
logging.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)

spice = nukleus.spice_path(['files/spice'])

spice = nukleus.spice_path(['files/spice'])

draw = Draw(library_path=['/usr/share/kicad/symbols'])
draw.add(Label("INPUT").rotate(180))
draw.add(Line())
draw.add(( dot1 := Dot()))
draw.add(Line().length(draw.unit*2).at(dot1))
draw.add(( dot2 := Dot()))

draw.add(Element("R1", "Device:R", value="100k").rotate(0))
draw.add(( dot3 := Dot()))
draw.add(Element("R2", "Device:R", value="100k").rotate(0))
draw.add(Element("GND", "power:GND"))

draw.add(Element("RV1", "Device:R_Potentiometer", value="100k").at(dot1).toy(get_pins(draw.R2[1])['2']).rotate(0))
draw.add(Line().down().at(get_pins(draw.RV1[1])['3']))
draw.add(Element("GND", "power:GND"))
draw.add(Line().at(dot3).tox(get_pins(draw.RV1[1])['2']))

draw.add(Line().at(dot2).length(draw.unit*2))
draw.add(Element("U1", "Amplifier_Operational:TL072", unit=1,
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='X',
                 Spice_Model='TL072c').anchor(2).mirror('x'))
draw.add(Line().at(get_pins(draw.U1[1])['1']))
draw.add(( dot4 := Dot()))
draw.add(Line())
draw.add(Label("OUTPUT"))
draw.add(Line().up().at(dot4).length(draw.unit*4))
draw.add(Element("R2", "Device:R", value="100k").tox(get_pins(draw.U1[1])['2']).rotate(270))
draw.add(Line().toy(get_pins(draw.U1[1])['2']))
draw.add(Line().tox(get_pins(draw.U1[1])['2']))
draw.add(Dot())
draw.add(Element("GND", "power:GND").at(get_pins(draw.U1[1])['3']))

draw.add(Element("U1", "Amplifier_Operational:TL072", unit=2, on_schema=False).at((102, 50)))
draw.add(Element("U1", "Amplifier_Operational:TL072", unit=3, on_schema=False).at((120, 50)))
draw.add(Element("+15V", "power:+15V", on_schema=False).at(get_pins(draw.U1[3])['8']))
draw.add(Element("-15V", "power:-15V", on_schema=False).at(get_pins(draw.U1[3])['4']).rotate(180))

plot(draw, 'attenuverter.pdf', scale=20)
