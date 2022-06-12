from typing import Any, Dict
import sys

import subprocess

import matplotlib

matplotlib.use('module://matplotlib-backend-kitty')
import matplotlib.pyplot as plt

sys.path.append('src')
sys.path.append('../src')

from nukleus.AbstractParser import AbstractParser
from nukleus.Notebook import Markdown, Notebook
from nukleus.Schema import Schema
import nukleus as nl
from nukleus.draw import Draw, Dot, Label, Line, Element
from nukleus.plot.PlotMatplotlib import PlotMatplotlib
from nukleus.spice.Potentiometer import Potentiometer
from nukleus.plot.PlotSvgWrite import PlotSvgWrite
from nukleus.plot.PlotCairo import PlotCairo

nl.set_spice_path(['samples/files/spice'])
nl.set_library_path(['/usr/share/kicad/symbols'])
nl.Registry().PLOTTER = PlotSvgWrite

def get_buffer(consumer: AbstractParser) -> None:
    with nl.draw(consumer) as draw:
        draw.add(Label("INPUT").rotate(180))
        draw.add(Line())
        draw.add(in_dot := Dot())
        draw.add(Line())
        draw.add(Element("R2", "Device:R", value="100k").rotate(90))
        draw.add(Element("C1", "Device:C", value="47n").rotate(90))
        draw.add(Line())
        draw.add(u1_dot_in := Dot())
        draw.add(Line())
        draw.add(Element("U1", "4xxx:4069", value="U1", unit=1,
                     Spice_Netlist_Enabled='Y',
                     Spice_Primitive='X',
                     Spice_Model='4069UB').anchor(1))
        draw.add(Line())
        draw.add(u1_dot_out := Dot())
        draw.add(Element("C5", "Device:C", value="10u").rotate(90))
        draw.add(Line())
        draw.add(out_dot := Dot())
        draw.add(Line())
        draw.add(Label("OUTPUT"))

        draw.add(Element("R1", "Device:R", value="1Meg").at(in_dot))
        draw.add(Element("GND", "power:GND"))

        draw.add(Element("R5", "Device:R", value="100k").at(out_dot))
        draw.add(Element("GND", "power:GND"))

        draw.add(Line().up().at(u1_dot_out).length(draw.unit*4))
        draw.add(Element("R3", "Device:R", value="100k").rotate(270).tox(u1_dot_in))
        draw.add(Line().down().toy(u1_dot_in))

        draw.add(Element("U1", "4xxx:4069", unit=7, on_schema=False).at((102, 50)))
        draw.add(Element("+5V", "power:+5V", on_schema=False).at(nl.pins(draw.U1[1])['14']))
        draw.add(Element("GND", "power:GND", on_schema=False).at(nl.pins(draw.U1[1])['7']).rotate(180))


class CmosBufferNotebook(Notebook):
    def __init__(self, frontmatter: Dict[str, Any]):
        super().__init__(frontmatter)

    def run(self):

        self.append(Markdown("The basic usage and pin mapping is explained in the datasheet [[1]](https://www.ti.com/lit/ds/schs054e/schs054e.pdf). It is not very common to use this chip for linear amplification, especially in our days where opamps are very cheap to get. But there is also an application note [[2]](http://www.sdiy.org/philgallo/hfvco/AN-0088.pdf) that explains the basic usage. It will not go into too many details, we will have to figure out some details on our own."))

        self.append(Markdown("For linear amplification only the unbuffered (UBE) chip can be used, the buffered chip will produce a binary output. Also, the chip should be powered by +5V/GND. With higher voltage, the heat dissipation will be too big and the chip will be damaged. the chip is powered on pins 7 and 14 with +5V and Ground. the other pins can be used as an amplifier."))

        #draw the cmos buffer
        writer = nl.SexpWriter()
        circuit = nl.Circuit(writer)
        plot = nl.SchemaPlot('cmos_buffer.svg', 297, 210, 600, theme='console', scale=10, child=circuit, border=False)
        get_buffer(plot)
        self.append(Markdown('![CMOS Buffer](cmos_buffer.svg)'))

        pot = Potentiometer("Potentiometer", 100000000, 1)
        circuit.subcircuit(pot)
        circuit.V("1", "+5V", "GND", "DC 5V")
        circuit.V("2", "INPUT", "GND", "DC 5 AC 2.5V SIN(0 5V 1k)")
        print(circuit)

        with nl.spice(circuit) as spice:
#for s in np.arange( 1, 0, -0.01 ):
            pot.wiper(0.2)

            with plt.style.context('dark_background'):
                vectors = spice.transient('10u', '2m', '0m')
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.plot(vectors['time']*1000, vectors['input'])
                ax.plot(vectors['time']*1000, vectors['output'])
                plt.savefig('cmos_buffer_simulation.svg')

        self.append(Markdown('![CMOS Buffer Simulation](cmos_buffer_simulation.svg)'))


        with open('kicad_file.kicad_sch', 'w') as f:
            f.write(str(writer))

frontmatter = {
        "author": "spielhuus",
        "categories": [
            "article"
        ],
        "date": "2021-01-10",
        "excerpt": "The CD4069UB device consists of six CMOS inverter circuits. These devices are intended for all general-purpose inverter applications. It is not ideal for linear amplification, but can be used as such and will add a lot of soft-clipping. This makes this device special for musical usage and can be found in guitar distortion pedals <a href='http://www.runoffgroove.com/ubescreamer.html'>[3]</a> or the wasp filter <a href='https://www.schmitzbits.de/wasp.html'>[4]</a>.",
        "hero_image": "cd4069.jpg",
        "hero_mobile": "arbeitsplatz-hero_portrait.jpg",
        "image": "cd4069.jpg",
        "subtitle": "Linear amplification with the CD4069UBE.",
        "tags": [
            "grundlage"
        ],
        "title": "cmos",
        "version": "0"
    }

if __name__ == "__main__":
    template = CmosBufferNotebook(frontmatter)
    template.run()
    with open('cmos_buffer_markdown.md', 'w') as filp:
        filp.write(str(template))
    subprocess.call(['/usr/bin/mdcat', 'cmos_buffer_markdown.md'])
