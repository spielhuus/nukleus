import json
import logging
import os
import shutil
from pathlib import Path

import SCons.Builder
import SCons.Tool
from SCons.Errors import StopError
from SCons.Node import NodeList

import nukleus
from ..Bom import Bom
from ..PcbUtils import PCB, Layer
from ..SchemaPlot import SchemaPlot
from ..PlotPcb import drc, pcb, pdf
from ..Reports import combine_reports, report_parser
from ..Schema import Schema
from ..Netlist import Netlist
from ..AbstractParser import AbstractParser

# The Scons bindings

#def scons_pcb(target, source, env):
#    temp_dir = os.path.join(target[0].dir.abspath, 'temp')
#    shutil.rmtree(temp_dir, ignore_errors=True)
#    try:
#        os.makedirs(temp_dir)
#        pcb_object = PCB(source[0].abspath)
#        layer_names = env['NUKLEUS_ENVIRONMENT_VARS']['pcb']['layers']
#        layers = []
#        for layer in layer_names:
#            layers.append(Layer.from_name(pcb_object, layer))
#
#        pdf(pcb_object, target[0].abspath, layers, temp_dir)
#    finally:
#        shutil.rmtree(temp_dir, ignore_errors=True)


def gerbers(target, source, env):
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


def _board_name(name: str) -> str:
    return name.split('.')[0]


def parse_bom(source, target, env, report):

    _report = {}
    if 'project_name' in env:
        _report = {env['project_name']: {_board_name(source[0].name): report}}
    else:
        _report = {_board_name(source[0].name): report}

    bom_name = f'{target[0].abspath}-bom.json'
    with open(bom_name, 'w') as file:
        file.write(json.dumps(_report))
    return bom_name
#
#
#def scons_drc(target, source, env):
#    pcb_object = PCB(source[0].abspath)
#    tmp_file = os.path.join(target[0].dir.abspath, 'drc_tmp.txt')
#    drc(pcb_object, tmp_file)
#    res_drc = {}
#    with open(tmp_file, 'r') as file:
#        report_parser(file.read(), res_drc)
#    report = {}
#    if 'project_name' in env:
#        report = {env['project_name']: {_board_name(source[0].name): res_drc}}
#    else:
#        report = {_board_name(source[0].name): res_drc}
#
#    os.remove(tmp_file)
#    with open(target[0].abspath, 'w') as file:
#        file.write(json.dumps(report))
#
#
#def scons_erc(target, source, env):
#    schema = Schema()
#    parser = ParserV6()
#    parser.schema(schema, source[0].abspath)
#    netlist = Netlist(schema)
#
#    res_erc = netlist.erc()
#    report = {}
#    if 'project_name' in env:
#        report = {env['project_name']: {_board_name(source[0].name): res_erc}}
#    else:
#        report = {_board_name(source[0].name): res_erc}
#
#    with open(target[0].abspath, 'w') as file:
#        file.write(json.dumps(report))
#
#
#def scons_reports(target, source, env):
#    source_files = []
#    for path in source:
#        source_files.append(path.abspath)
#
#    with open(target[0].abspath, 'w') as file:
#        json.dump(combine_reports(source_files), file)

def get_schema_name(filename):
    if not filename.endswith('.kicad_pro'):
        raise ValueError(f'not a kicad project file: {filename}')
    return f'{filename.rstrip(".kicad_pro")}.kicad_sch'


def scons_nukleus(target, source, env):
    files = []
    visitor: AbstractParser|None = None
    bom: Bom|None = None
    for build_target in env['NUKLEUS_TARGETS']:
        print(build_target)
        if build_target == 'schema':
            schema_name = f'{target[0].abspath}-schema.svg'
            visitor = SchemaPlot(schema_name, 297, 210, 600, child=visitor) #TODO make filename configurable
            target.append(schema_name)
        if build_target == 'bom':
            bom = visitor = Bom(child=visitor)

    if not visitor:
        raise ValueError('no target set')
    with nukleus.schema(get_schema_name(source[0].abspath), visitor) as _:
        pass

    if bom:
        target.append(parse_bom(source, target, env, bom.bom()))


def generate(env):

    # initialize the logger
    logging.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=logging.INFO)
    logging.getLogger().setLevel(logging.INFO)

    env.SetDefault(NUKLEUS_CONTEXT={})
    env.SetDefault(NUKLEUS_ENVIRONMENT_VARS={})
    env.SetDefault(NUKLEUS_TEMPLATE_SEARCHPATH=[])

#    kiscan = SCons.Script.Scanner(function = kicad_scan, skeys = ['.pro'])
    env['BUILDERS']['nukleus'] = SCons.Builder.Builder(action=scons_nukleus)
#    env['BUILDERS']['pcb'] = SCons.Builder.Builder(action=scons_pcb)
#    env['BUILDERS']['gerbers'] = SCons.Builder.Builder(action=scons_gerbers)
#    env['BUILDERS']['drc'] = SCons.Builder.Builder(action=scons_drc)
#    env['BUILDERS']['erc'] = SCons.Builder.Builder(action=scons_erc)
#    env['BUILDERS']['bom'] = SCons.Builder.Builder(action=scons_bom)
#    env['BUILDERS']['reports'] = SCons.Builder.Builder(action=scons_reports)
#    env['BUILDERS']['report2xunit'] = SCons.Builder.Builder(action=xunit)
