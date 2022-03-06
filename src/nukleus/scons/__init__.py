from typing import List

import os
import sys
import json
import shutil

import SCons.Builder
import SCons.Tool
from SCons.Errors import StopError

from ..PcbUtils import Layer, PCB
from ..PlotPcb import pcb, pdf, drc
from ..Schema import Schema
from ..ParserV6 import ParserV6
from ..Bom import bom
from ..Plot import plot

## The Scons bindings
def scons_bom(target, source, env):
    schema = Schema()
    parser = ParserV6()
    parser.schema(schema, source[0].abspath)
    res = bom(schema)
    with open(target[0].abspath, 'w') as file:
        file.write(json.dumps(res))

def scons_schema(target, source, env):
    schema = Schema()
    parser = ParserV6()
    parser.schema(schema, source[0].abspath)
    plot(schema, target[0].abspath, border=True)

def scons_pcb(target, source, env):
    temp_dir = os.path.join(target[0].dir.abspath, 'temp')
    shutil.rmtree(temp_dir, ignore_errors=True)
    try:
        os.makedirs(temp_dir)
        pcb_object = PCB(source[0].abspath)
        layer_names = env['NUKLEUS_ENVIRONMENT_VARS']['pcb']['layers']
        layers = []
        for layer in layer_names:
            layers.append(Layer.from_name(pcb_object, layer))

        pdf(pcb_object, target[0].abspath, layers, temp_dir)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def scons_gerbers(target, source, env):
    temp_dir = os.path.join(target[0].dir.abspath, 'temp')
    shutil.rmtree(temp_dir, ignore_errors=True)
    try:
        os.makedirs(temp_dir)
        pcb_object = PCB(source[0].abspath)
        layer_names = env['NUKLEUS_ENVIRONMENT_VARS']['pcb']['layers']
        layers = []
        for layer in layer_names:
            layers.append(Layer.from_name(pcb_object, layer))

        pcb(pcb_object, target[0].abspath, layers, temp_dir)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def scons_drc(target, source, env):
    pcb_object = PCB(source[0].abspath)
    drc(pcb_object, target[0].abspath)

def generate(env):

    env.SetDefault(NUKLEUS_CONTEXT={})
    env.SetDefault(NUKLEUS_ENVIRONMENT_VARS={})
    env.SetDefault(NUKLEUS_TEMPLATE_SEARCHPATH=[])

#    kiscan = SCons.Script.Scanner(function = kicad_scan, skeys = ['.pro'])
#    env['BUILDERS']['preflight'] = SCons.Builder.Builder(action=kibot_preflight, source_scanner = kiscan)
    env['BUILDERS']['schema'] = SCons.Builder.Builder(action=scons_schema)
    env['BUILDERS']['bom'] = SCons.Builder.Builder(action=scons_bom)
    env['BUILDERS']['pcb'] = SCons.Builder.Builder(action=scons_pcb)
    env['BUILDERS']['gerbers'] = SCons.Builder.Builder(action=scons_gerbers)
    env['BUILDERS']['drc'] = SCons.Builder.Builder(action=scons_drc)
#    env['BUILDERS']['reports'] = SCons.Builder.Builder(action=kibot_combine_reports)
#    env['BUILDERS']['report2xunit'] = SCons.Builder.Builder(action=xunit)
