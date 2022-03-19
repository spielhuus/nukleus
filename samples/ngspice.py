import sys

sys.path.append('src')
sys.path.append('../src')

import matplotlib.pyplot as plt

import os
import nukleus

schema = nukleus.load_schema('files/summe_v6/main.kicad_sch')
cwd = os.getcwd() + "/files/spice"
models = nukleus.SpiceModel.load_spice_models([cwd])

circuit = nukleus.Circuit()
circuit.models(models)
#for c in (VoltageDivider(R=100000, w=0.5, name='voltage_divider_1'),
#          VoltageDivider(R=100000, w=0.5, name='voltage_divider_2'),
#          VoltageDivider(R=100000, w=0.5, name='voltage_divider_3'),
#          VoltageDivider(R=100000, w=0.5, name='voltage_divider_4'),
#          JackIn(name='IN_1', value='AC 5 DC 5 SINE(0 5 1k)'),
#          JackIn(name='IN_2', value='AC 5 DC 5 SINE(0 5 2k)'),
#          JackIn(name='IN_3', value='AC 5 DC 5 SINE(0 5 3k)'),
#          JackIn(name='IN_4', value='AC 5 DC 5 SINE(0 5 4k)'),
#          JackOut(name='OUT_1'),
#          JackOut(name='OUT_2'),
#          JackOut(name='OUT_3'),
#          JackOut(name='OUT_4'),
#          JackOut(name='OUT')):
#    circuit.subcircuit(c)

list = nukleus.Spice.netlist(schema)
nukleus.Spice.schema_to_spice(schema, circuit, list)
circuit.V("1", "+15V", "GND", "DC 15V")
circuit.V("2", "-15V", "GND", "DC -15V")
circuit.V("3", "INPUT", "GND", "DC 5V AC 5 SIN(0 5V 1k)")

print(circuit)

spice = nukleus.spice.ngspice()
print(spice.cmd("version"))
print(spice.circuit(circuit.__str__()))
vectors = spice.transient()
fig, ax = plt.subplots(figsize=(8, 6))
# Add a bit of margin since matplotlib chops off the text otherwise
ax.set_xmargin(0.1)
ax.set_ymargin(0.1)
ax.plot(vectors['time']*1000, vectors['input'])
ax.plot(vectors['time']*1000, vectors['output'])
#ax.plot(vectors['time']*1000, vectors['input'])
plt.show()
