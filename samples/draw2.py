import sys
import os

import matplotlib.pyplot as plt
import logging

from nukleus.SexpWriter import SexpWriter

sys.path.append('src')
sys.path.append('../src')

import nukleus
from nukleus.draw import Dot, Label, Line, Element
from nukleus import Circuit
from nukleus.Netlist import Netlist
from nukleus.spice.Potentiometer import Potentiometer
from nukleus.SchemDraw import SchemDraw
from nukleus.transform import get_pins

import numpy as np

# initialize the logger
logging.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

spice = nukleus.spice_path(['files/spice'])
cwd = os.getcwd() + "/files/spice"
cwd2 = "/home/etienne/Documents/elektrophon/lib/spice"
models = nukleus.SpiceModel.load_spice_models([cwd2])

draw = SchemDraw(library_path=['/usr/share/kicad/symbols'])
draw.add(Label("INPUT").rotate(180))
draw.add(Line())
draw.add(in_dot := Dot())
draw.add(Element("D1", "Diode:1N4148",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='D',
                 Spice_Model='D1N4148',
                 Spice_Node_Sequence='2 1').mirror('y').anchor('2'))
draw.add(Line().length(draw.unit*6))
draw.add(Element("U1", "Amplifier_Operational:TL072", unit=1,
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='X',
                 Spice_Model='TL072c').anchor(3))

draw.add(Element("R2", "Device:R", value="180k").at(in_dot).rotate(0))
draw.add(Element("GND", "power:GND"))

draw.add(Line().length(draw.unit*2).at(get_pins(draw.U1[0])['2']).left())
draw.add(reference_dot := Dot())
draw.add(Element("R3", "Device:R", value="10k"))
draw.add(Element("GND", "power:GND"))

draw.add(Line().length(draw.unit*2).at(reference_dot).up())
draw.add(Element("R4", "Device:R", value="50k").rotate(180))
draw.add(Element("+15V", "power:+15V"))

draw.add(Line().length(draw.unit).at(get_pins(draw.U1[0])['1']).right())
draw.add(opamp_dot := Dot())

draw.add(Line().length(draw.unit*2).up())
draw.add(Element("D2", "Diode:1N4148",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='D',
                 Spice_Model='D1N4148',
                 Spice_Node_Sequence='2 1').mirror('y').anchor('2'))
draw.add(Element("RV1", "Device:R_Potentiometer", value="1Meg",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='X',
                 Spice_Model='Potentiometer1').anchor(1).rotate(90).mirror('x'))
draw.add(Line().length(draw.unit))
draw.add(Line().toy(get_pins(draw.RV1[0])['2']))
draw.add(rv1_dot := Dot())
draw.add(Line().toy(opamp_dot))
draw.add(reg_dot := Dot())
draw.add(Line().at(rv1_dot).tox(get_pins(draw.RV1[0])['2']))

draw.add(Line().length(draw.unit*2).down().at(opamp_dot))
draw.add(Element("D3", "Diode:1N4148",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='D',
                 Spice_Model='D1N4148',
                 Spice_Node_Sequence='2 1').mirror('y').anchor('2'))
draw.add(Element("RV2", "Device:R_Potentiometer", value="1Meg",
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='X',
                 Spice_Model='Potentiometer2').anchor(1).rotate(90).mirror('x'))
draw.add(Line().length(draw.unit))
draw.add(Line().toy(get_pins(draw.RV2[0])['3']))
draw.add(rv2_dot := Dot())
draw.add(Line().toy(opamp_dot))
draw.add(reg_dot := Dot())

draw.add(Line().at(rv2_dot).toy(get_pins(draw.RV2[0])['2']))
draw.add(Line().tox(get_pins(draw.RV2[0])['2']))

draw.add(Line().at(reg_dot).length(draw.unit*2))
draw.add(cap_dot := Dot())
draw.add(Line().length(draw.unit*2))
draw.add(Element("U1", "Amplifier_Operational:TL072", unit=2,
                 Spice_Netlist_Enabled='Y',
                 Spice_Primitive='X',
                 Spice_Model='TL072c').anchor(5).mirror('x'))

draw.add(Element("C1", "Device:C", value="1u").rotate(0).at(cap_dot))
draw.add(Element("GND", "power:GND"))

draw.add(Line().at(get_pins(draw.U1[1])['6']).up().length(draw.unit*3))
draw.add(Line().tox(get_pins(draw.U1[1])['7']))
draw.add(Line().toy(get_pins(draw.U1[1])['7']))
draw.add(out_dot := Dot())

draw.add(Line().right())
draw.add(Element("R5", "Device:R", value="1k").rotate(90))
draw.add(Label("OUTPUT").rotate(0))

draw.add(Element("U1", "Amplifier_Operational:TL072", unit=3, on_schema=False).at((120, 50)))
draw.add(Element("+15V", "power:+15V", on_schema=False).at(get_pins(draw.U1[2])['8']))
draw.add(Element("-15V", "power:-15V", on_schema=False).at(get_pins(draw.U1[2])['4']).rotate(180))

print("outputsexp")
sexpwriter = SexpWriter()
draw.produce(sexpwriter)

print("spice")
circuit = nukleus.Circuit()
circuit.models(models)
netlist = Netlist(draw)
draw.produce(netlist)
pot1 = Potentiometer("Potentiometer1", 1000000, 0.01)
pot2 = Potentiometer("Potentiometer2", 1000000, 0.99)
circuit.subcircuit(pot1)
circuit.subcircuit(pot2)

nukleus.plot('envelope.svg', draw)

netlist.spice(circuit)
circuit.V("1", "+15V", "GND", "DC 15V")
circuit.V("2", "-15V", "GND", "DC -15V")
circuit.V("3", "INPUT", "GND", "DC 0 AC 0 PULSE(0 5 20m 0m 0m 60m 200m)")


print(f'--------------\n {circuit} \n---------------')

spice = nukleus.spice.ngspice()
spice.circuit(circuit.__str__())
print(spice.cmd("version"))
print(spice.circuit(circuit.__str__()))
ar_analysis = spice.transient('0.5ms', '200ms', '0ms')

fig_buffer, ax1_buffer = plt.subplots()

ax1_buffer.set_xlabel('time [ms]')
ax1_buffer.set_ylabel('amplitude [V]')
ax1_buffer.plot(ar_analysis['time'], ar_analysis['input'], color='Grey')
ax1_buffer.plot(ar_analysis['time'], ar_analysis['output'], color='Red')

ax1_buffer.legend(('trigger', 'envelope'), loc=(0.75,0.8))

plt.grid()
plt.tight_layout()
plt.show()

