import os
import shutil
import logging
import zipfile
from PyPDF2 import PdfFileMerger, PdfFileReader

#import sys
#sys.path.append('/usr/lib/python3.10/site-packages/')

import pcbnew

from .PcbUtils import PCB, Layer

def drc(pcb: PCB, target: str) -> None:
    pcbnew.WriteDRCReport(pcb.board, target, pcbnew.EDA_UNITS_MILLIMETRES, True)

def pcb(pcb: PCB, target, layers, temp_dir):
    output_files = []
    pcb.set_plot_directory(temp_dir)
    pcb.plot_options.SetDrillMarksType(
        pcbnew.PCB_PLOT_PARAMS.NO_DRILL_SHAPE)

    for layer in layers:
        logging.debug('plotting layer {} ({}) to Gerber'.format(
            layer.get_name(), layer.layer_id))
        output_filename = layer.plot(pcbnew.PLOT_FORMAT_GERBER)
        output_files.append(output_filename)

    drill_file = pcb.plot_drill()
    if os.path.isfile(drill_file):  # No drill file is generated if no holes exist
        output_files.append(drill_file)

    zip_file_name = os.path.join(target)
    with zipfile.ZipFile(zip_file_name, 'w') as zfile:
        for file in output_files:
            zfile.write(file, os.path.relpath(file, temp_dir))

def pdf(pcb: PCB, target, layers, temp_dir):
    merger = PdfFileMerger()
    pcb.set_plot_directory(temp_dir)
    pcb.plot_options.SetDrillMarksType(
        pcbnew.PCB_PLOT_PARAMS.NO_DRILL_SHAPE)

    for layer in layers:
        logging.debug('plotting layer {} ({}) to PDF'.format(
            layer.get_name(), layer.layer_id))
        output_filename = layer.plot(pcbnew.PLOT_FORMAT_PDF)
        with open(output_filename, 'rb') as file:
            merger.append(PdfFileReader(file), bookmark=layer.get_name())

    drill_file = pcb.plot_drill_map()
    if os.path.isfile(drill_file):  # No drill file is generated if no holes exist
        with open(drill_file, 'rb') as file:
            merger.append(PdfFileReader(file), bookmark='Drill map')

    merger.write(target)



