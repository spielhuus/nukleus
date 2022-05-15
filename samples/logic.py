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

# initialize the logger
logging.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)

cwd = os.getcwd() + "/files/spice"
models = nukleus.SpiceModel.load_spice_models([cwd])

draw = Draw(library_path=['/usr/share/kicad/symbols'])

for i in range(4):
    draw.add(switch_in := Element(f"J{i+1}", "Connector:AudioJack2_SwitchT").rotate(0).at((10,i*15)))
    draw.add(Element("GND", "power:GND").at(get_pins(switch_in.element)['S']).rotate(90))
    draw.add(switch_out := Element(f"J{i+5}", "Connector:AudioJack2_SwitchT").mirror('y').at((40,i*15)))
    draw.add(Element("GND", "power:GND").at(get_pins(switch_out.element)['S']).rotate(270))

plot(draw, 'logic.pdf', theme='notebook')
