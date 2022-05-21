import sys

import logging
import matplotlib

matplotlib.use('module://matplotlib-backend-kitty')
import matplotlib.pyplot as plt
import networkx as nx

sys.path.append('src')
sys.path.append('../src')

from nukleus.Circuit import Circuit
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

writer = nl.SexpWriter()
circuit = Circuit(writer)
with nl.schema('files/summe_v6/main.kicad_sch', circuit) as _:
    pass

print(circuit)

pos=nx.spring_layout(circuit.graph)
subax1 = plt.subplot(121)
nx.draw(circuit.graph, pos, with_labels=True, font_weight='bold')
#subax2 = plt.subplot(122)
#nx.draw_shell(netlist.graph, pos, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

plt.show()
