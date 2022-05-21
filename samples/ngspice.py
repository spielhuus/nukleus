import sys
import os

import matplotlib

matplotlib.use('module://matplotlib-backend-kitty')
import matplotlib.pyplot as plt

sys.path.append('src')
sys.path.append('../src')
import nukleus as nl
from nukleus.Circuit import Circuit

nl.set_spice_path([os.getcwd() + "/files/spice"])

vectors = {}
with nl.schema('files/summe_v6/main.kicad_sch', Circuit()) as circuit:
    circuit.V("1", "+15V", "GND", "DC 15V")
    circuit.V("2", "-15V", "GND", "DC -15V")
    circuit.V("3", "INPUT", "GND", "DC 5V AC 5 SIN(0 5V 1k)")

    with nl.spice(circuit) as spice:
        vectors = spice.transient('1u', '1m', '0')

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(vectors['time']*1000, vectors['input'])
ax.plot(vectors['time']*1000, vectors['output'])
plt.show()
