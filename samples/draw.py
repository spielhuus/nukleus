import sys
sys.path.append('src')
sys.path.append('../src')

import nukleus
from nukleus.draw import Draw, Dot, Label, Line, Element
from nukleus import Circuit
from nukleus.Plot import plot
from nukleus.model.Utils import get_pins
from nukleus.Netlist import Netlist

spice = nukleus.spice_path(['files/spice'])

draw = Draw(library_path=['/usr/share/kicad/symbols'])
draw.add(Label("INPUT"))
draw.add(Line())
draw.add(Element("R1", "Device:R", value="100k").rotate(90))
draw.add(Line())
draw.add(Element("U1", "Amplifier_Operational:TL072", unit=1,
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='X',
                 Spice_Model='TL072c').anchor(2).mirror('x'))
draw.add(Line().at(get_pins(draw.U1[1])['1']))
draw.add(( dot1 := Dot()))
draw.add(Line())
draw.add(Label("OUTPUT"))
draw.add(Line().up().at(dot1).length(draw.unit*4))
draw.add(Element("R2", "Device:R", value="100k").rotate(270))
draw.add(Line().tox(get_pins(draw.U1[1])['2']))
draw.add(Line().toy(get_pins(draw.U1[1])['2']))
draw.add(Line().tox(get_pins(draw.U1[1])['2']))
draw.add(Dot())
draw.add(Element("GND", "power:GND").at(get_pins(draw.U1[1])['3']))

draw.add(Element("U1", "Amplifier_Operational:TL072", unit=2, on_schema=False).at((100, 50)))
draw.add(Element("U1", "Amplifier_Operational:TL072", unit=3, on_schema=False).at((120, 50)))
draw.add(Element("+15V", "power:+15V", on_schema=False).at(get_pins(draw.U1[3])['8']))
draw.add(Element("-15V", "power:-15V", on_schema=False).at(get_pins(draw.U1[3])['4']).rotate(180))

#print(draw.sexp())

nl = Netlist(draw)
circuit = Circuit()
circuit.models(spice)
circuit.V('1', 'INPUT', 'GND', 'DC 5 AC 5 SINE(5 100)')
circuit.V('2', '+15V', 'GND', 'DC 15')
circuit.V('3', '-15V', 'GND', 'DC -15')
nl.spice(circuit)
print(circuit)

#p = nukleus.draw.plot()
plot(draw, 'schema.pdf', scale=5)
