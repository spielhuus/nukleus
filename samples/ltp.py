import sys
import os

import matplotlib.pyplot as plt
import logging

sys.path.append('src')
sys.path.append('../src')

import nukleus as nl
from nukleus.draw import Draw, Dot, Label, Line, Element
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

    draw.add(label_x := Label("X").rotate(180))
    draw.add(Line())
    draw.add(( dot_in_x := Dot()))
    draw.add(Line())
    draw.add(Element("Q1", "Transistor_BJT:BC547", value="BC547",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='Q',
                 Spice_Model='BC547B').anchor(2).rotate(0))

    draw.add(Line().length(draw.unit).down().at(nl.pins(draw.Q1[0])['3']))
    draw.add(Line().length(draw.unit).left().length(draw.unit*4))
    draw.add(( dot_tail_1 := Dot()))
    draw.add(Line().length(draw.unit).left().length(draw.unit*4))
    draw.add(Line().length(draw.unit).up())
    draw.add(Element("Q2", "Transistor_BJT:BC547", value="BC547",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='Q',
                 Spice_Model='BC547B').mirror('y').anchor(3).rotate(0))

    # the pair
    draw.add(Line().at(nl.pins(draw.Q2[0])['2']))
    draw.add(( dot_pair_gnd := Dot()))
    draw.add(Element("GND", "power:GND"))
    draw.add(Line().at(dot_pair_gnd))
    draw.add(Element("Q3", "Transistor_BJT:BC547", value="BC547",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='Q',
                 Spice_Model='BC547B').anchor(2).rotate(0))
    draw.add(Line().length(draw.unit).down().at(nl.pins(draw.Q3[0])['3']))
    draw.add(Line().length(draw.unit).left().length(draw.unit*4))
    draw.add(( dot_tail_2 := Dot()))
    draw.add(Line().length(draw.unit).left().length(draw.unit*4))
    draw.add(Line().length(draw.unit).up())
    draw.add(Element("Q4", "Transistor_BJT:BC547", value="BC547",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='Q',
                 Spice_Model='BC547B').mirror('y').anchor(3).rotate(0))


    draw.add(Line().length(draw.unit).down().at(dot_tail_1))
    draw.add(Element("Q5", "Transistor_BJT:BC547", value="BC547",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='Q',
                 Spice_Model='BC547B').mirror('').anchor(1).rotate(0))
    draw.add(Line().length(draw.unit).down().at(nl.pins(draw.Q5[0])['3']))
    draw.add(Line().right().tox(dot_pair_gnd))
    draw.add(dot_tail := Dot())
    draw.add(Line().down())
    draw.add(Element("R3", "Device:R", value="720").rotate(0))
    draw.add(Element("-15V", "power:-15V").rotate(180))

    draw.add(Line().length(draw.unit).down().at(dot_tail_2))
    draw.add(Element("Q6", "Transistor_BJT:BC547", value="BC547",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='Q',
                 Spice_Model='BC547B').mirror('y').anchor(1).rotate(0))
    draw.add(Line().length(draw.unit).down().at(nl.pins(draw.Q6[0])['3']))
    draw.add(Line().left().tox(dot_pair_gnd))
    draw.add(Line().left().at(nl.pins(draw.Q6[0])['2']))
    draw.add(Element("R4", "Device:R", value="2.2k").rotate(0))
    draw.add(Element("+7.5V", "power:+7.5V", value="vBias").rotate(180))

    draw.add(Line().length(draw.unit).right().at(nl.pins(draw.Q5[0])['2']))
    draw.add(y_bias := Dot())
    draw.add(Element("C", "Device:C", value="220n").rotate(270).tox(label_x))
    draw.add(Label("Y").rotate(180))
    draw.add(Element("R5", "Device:R", value="2.2k").rotate(0).at(y_bias))
    draw.add(Element("+7.5V", "power:+7.5V", value="vBias").rotate(180))


#connect the head
    draw.add(Line().length(draw.unit).up().at(nl.pins(draw.Q1[0])['1']))
    draw.add(( dot_con_a := Dot()))
    draw.add(Line().length(draw.unit*1.5).up())
    draw.add(( dot_out_a := Dot()))
    draw.add(Line().length(draw.unit).up())
    draw.add(Element("R1", "Device:R", value="720").rotate(180))
    draw.add(Line().length(draw.unit).up())
    draw.add(Line().tox(dot_pair_gnd))
    draw.add(Dot())
    draw.add(Element("+15V", "power:+15V"))

    draw.add(Line().length(draw.unit*1.5).up().at(nl.pins(draw.Q4[0])['1']))
    draw.add(( dot_con_b := Dot()))
    draw.add(Line().length(draw.unit).up())
    draw.add(( dot_out_b := Dot()))
    draw.add(Line().length(draw.unit).up())
    draw.add(Element("R2", "Device:R", value="720").rotate(180))
    draw.add(Line().length(draw.unit).up())
    draw.add(Line().tox(dot_pair_gnd))

    draw.add(Line().at(dot_con_a).tox(nl.pins(draw.Q3[0])['1']))
    draw.add(Line().toy(nl.pins(draw.Q3[0])['1']))
    draw.add(Line().at(dot_con_b).tox(nl.pins(draw.Q2[0])['1']))
    draw.add(Line().toy(nl.pins(draw.Q2[0])['1']))

    draw.add(Line().length(draw.unit*2).at(dot_out_a))
    draw.add(Label("OUTa").rotate(0))
    draw.add(Line().length(draw.unit*2).right().at(dot_out_b))
    draw.add(Label("OUTb").rotate(180))

    draw.add(Line().at(nl.pins(draw.Q4[0])['2']).down().length(draw.unit*2))
    draw.add(Line().tox(dot_in_x))
    draw.add(Line().toy(dot_in_x))

#draw.add(Element("R3", "Device:R", value="33k").at(dot1).rotate(0))
#draw.add(Line().down())
#draw.add(( dot2 := Dot()))
#draw.add(Line().down())
#draw.add(Element("R4", "Device:R", value="15k").rotate(0))
#
#draw.add(Line().at(dot2).length(draw.unit*2).right())
#draw.add(Line().down().length(draw.unit))
#draw.add(Element("Q3", "Transistor_BJT:BC548", value="BC548",
#                 Spice_Netlist_Enabled='Y',
#                 Spice_Primitive='Q',
#                 Spice_Model='BC547B').mirror('x').anchor(3).rotate(0))
#draw.add(Element("GND", "power:GND").at(nl.pins(draw.Q3[1])['1']))
#draw.add(Line().left().length(draw.unit).at(nl.pins(draw.Q3[1])['2']))
#draw.add(Label("Y").rotate(180))
#
#draw.add(Line().left().length(draw.unit).at(dot_out_a))
#draw.add(Label("OUTa").rotate(0))
#draw.add(Line().right().length(draw.unit).at(dot_out_b))
#draw.add(Label("OUTb").rotate(180))


with nl.circuit(netlist) as circuit:
    circuit.V("1", "+15V", "GND", "DC 15V")
    circuit.V("2", "-15V", "GND", "DC -15V")
    circuit.V("3", "x", "GND", "DC 5V AC 5 SIN(0 20m 100)")
    circuit.V("4", "y", "GND", "DC 5V AC 5 SIN(0 10m 1k)")
    circuit.V("5", "Vbias", "GND", "DC -7.5V")
    print(circuit)

    with nl.spice(circuit) as spice:
        vectors = spice.transient('10u', '10m', '0m')

plt.show()

fig, ax = plt.subplots(figsize=(8, 6))
#ax.plot(vectors['time']*1000, vectors['x'])
ax.plot(vectors['time']*1000, vectors['x']*8)
ax.plot(vectors['time']*1000, vectors['outa'] - vectors['outb'])
plt.show()
