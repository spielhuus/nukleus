import sys
import os

import matplotlib
matplotlib.use('module://matplotlib-backend-kitty')
import matplotlib.pyplot as plt
import logging


sys.path.append('src')
sys.path.append('../src')

import nukleus as nl
from nukleus.draw import Dot, Label, Line, Element
from nukleus.spice.Potentiometer import Potentiometer
from nukleus.plot.PlotMatplotlib import PlotMatplotlib

# initialize the logger
logging.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

nl.set_spice_path(['files/spice'])
nl.set_library_path(['/usr/share/kicad/symbols'])
nl.Registry().PLOTTER = PlotMatplotlib

vectors = []
writer = nl.SexpWriter()
netlist = nl.Netlist(writer)
schem_fig, schem_ax = plt.subplots(figsize=(8, 6))

plot = nl.SchemaPlot(schem_ax, 297, 210, 600, child=netlist)
with nl.draw(plot) as draw:
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
                     Spice_Model='Potentiometer')
                        .at(dot1).toy(nl.pins(draw.R4[0])['2']).rotate(0))
    draw.add(Line().down().at(nl.pins(draw.RV1[0])['3']))
    draw.add(Element("GND", "power:GND"))
    draw.add(Line().at(dot3).tox(nl.pins(draw.RV1[0])['2']))

    draw.add(Line().at(dot2).length(draw.unit*2))
    draw.add(Element("R1", "Device:R", value="100k").rotate(90))
    draw.add(Line())
    draw.add(Element("U1", "Amplifier_Operational:TL072", unit=1,
                     Spice_Netlist_Enabled='Y',
                     Spice_Primitive='X',
                     Spice_Model='TL072c').anchor(2).mirror('x'))
    draw.add(Line().at(nl.pins(draw.U1[0])['1']))
    draw.add(( dot4 := Dot()))
    draw.add(Line())
    draw.add(Label("OUTPUT"))
    draw.add(Line().up().at(dot4).length(draw.unit*5))
    draw.add(Element("R2", "Device:R", value="100k")
                .tox(nl.pins(draw.U1[0])['2']).rotate(270))
    draw.add(Line().toy(nl.pins(draw.U1[0])['2']))
    draw.add(Line().tox(nl.pins(draw.U1[0])['2']))
    draw.add(Dot())

    draw.add(Line().at(nl.pins(draw.U1[0])['3']).left())
    draw.add(Line().toy(dot3))
    draw.add(Line().tox(dot3))

    draw.add(Element("U1", "Amplifier_Operational:TL072",
                     unit=2, on_schema=False).at((102, 50)))
    draw.add(Element("U1", "Amplifier_Operational:TL072",
                     unit=3, on_schema=False).at((120, 50)))
    draw.add(Element("+15V", "power:+15V", on_schema=False)
            .at(nl.pins(draw.U1[2])['8']))
    draw.add(Element("-15V", "power:-15V", on_schema=False)
            .at(nl.pins(draw.U1[2])['4']).rotate(180))

with nl.circuit(netlist) as circuit:
    pot = Potentiometer("Potentiometer", 100000, 0.3)
    circuit.subcircuit(pot)
    circuit.V("1", "+15V", "GND", "DC 15V")
    circuit.V("2", "-15V", "GND", "DC -15V")
    circuit.V("3", "INPUT", "GND", "DC 5V AC 5 SIN(0 5V 1k)")
    print(circuit)

    with nl.spice(circuit) as spice:
        #for s in np.arange( 1, 0, -0.01 ):
        pot.wiper(0.2)
        vectors = spice.transient('10u', '10m', '0m')

plt.show()

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xmargin(0.1)
ax.set_ymargin(0.1)
ax.plot(vectors['time']*1000, vectors['input'])
ax.plot(vectors['time']*1000, vectors['output'])
plt.show()
