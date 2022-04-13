import sys
import os

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
from nukleus.spice.Potentiometer import Potentiometer

import numpy as np

# initialize the logger
logging.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

spice = nukleus.spice_path(['files/spice'])

draw = Draw(library_path=['/usr/share/kicad/symbols'])
draw.add(Label("INPUT").rotate(180))
draw.add(Line())
draw.add(( dot1 := Dot()))
draw.add(Line().length(draw.unit*2).at(dot1))
draw.add(( dot2 := Dot()))

draw.add(Element("R3", "Device:R", value="47k").rotate(0))
draw.add(( dot3 := Dot()))
draw.add(Element("R4", "Device:R", value="47k").rotate(0))
draw.add(Element("GND", "power:GND"))

draw.add(Element("RV1", "Device:R_Potentiometer", value="100k",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='X',
                 Spice_Model='Potentiometer').at(dot1).toy(get_pins(draw.R4[1])['2']).rotate(0))
draw.add(Line().down().at(get_pins(draw.RV1[1])['3']))
draw.add(Element("GND", "power:GND"))
draw.add(Line().at(dot3).tox(get_pins(draw.RV1[1])['2']))

draw.add(Line().at(dot2).length(draw.unit*2))
draw.add(Element("R1", "Device:R", value="100k").rotate(90))
draw.add(Line())
draw.add(Element("U1", "Amplifier_Operational:TL072", unit=1,
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='X',
                 Spice_Model='TL072c').anchor(2).mirror('x'))
draw.add(Line().at(get_pins(draw.U1[1])['1']))
draw.add(( dot4 := Dot()))
draw.add(Line())
draw.add(Label("OUTPUT"))
draw.add(Line().up().at(dot4).length(draw.unit*5))
draw.add(Element("R2", "Device:R", value="100k").tox(get_pins(draw.U1[1])['2']).rotate(270))
draw.add(Line().toy(get_pins(draw.U1[1])['2']))
draw.add(Line().tox(get_pins(draw.U1[1])['2']))
draw.add(Dot())

draw.add(Line().at(get_pins(draw.U1[1])['3']).left())
draw.add(Line().toy(dot3))
draw.add(Line().tox(dot3))

draw.add(Element("U1", "Amplifier_Operational:TL072", unit=2, on_schema=False).at((102, 50)))
draw.add(Element("U1", "Amplifier_Operational:TL072", unit=3, on_schema=False).at((120, 50)))
draw.add(Element("+15V", "power:+15V", on_schema=False).at(get_pins(draw.U1[3])['8']))
draw.add(Element("-15V", "power:-15V", on_schema=False).at(get_pins(draw.U1[3])['4']).rotate(180))

plot(draw, 'attenuverter.pdf', scale=20)

print(draw.sexp())

cwd = os.getcwd() + "/files/spice"
models = nukleus.SpiceModel.load_spice_models([cwd])

circuit = nukleus.Circuit()
circuit.models(models)
pot = Potentiometer("Potentiometer", 100000, 0.3)
circuit.subcircuit(pot)
netlist = Netlist(draw)
for cord, net in netlist.nets.items():
    print(f'{cord} {net}')

netlist.spice(circuit)
circuit.V("1", "+15V", "GND", "DC 15V")
circuit.V("2", "-15V", "GND", "DC -15V")
circuit.V("3", "INPUT", "GND", "DC 5V AC 5 SIN(0 5V 1k)")

print(circuit)

for s in np.arange( 1, 0, -0.01 ):
    pot.wiper(s)
    spice = nukleus.spice.ngspice()
    spice.circuit(circuit.__str__())
#vectors = spice.transient('10u', '20m', '0m')
    vectors = spice.op()

    #print(vectors['output'])

#fig, ax = plt.subplots(figsize=(8, 6))
## Add a bit of margin since matplotlib chops off the text otherwise
#ax.set_xmargin(0.1)
#ax.set_ymargin(0.1)
##ax.plot(vectors['time']*1000, vectors['input'])
#ax.plot(vectors['time']*1000, vectors['output'])
##ax.plot(vectors['time']*1000, vectors['input'])
#plt.show()
