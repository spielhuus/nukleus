from typing import List

import os
import sys

from . import draw, model, spice
from .Circuit import Circuit
from .Library import Library
from .ParserV6 import ParserV6
from .Plot import plot
from .Schema import Schema
from .Spice import netlist, schema_to_spice
from .SpiceModel import load_spice_models

import SCons.Builder
import SCons.Tool
from SCons.Errors import StopError

#SYMBOL_SEARCH_PATH_POSIX = [
#    '/usr/share/kicad/symbols',
#    '/usr/local/share/kicad/symbols'
#]
#SYMBOL_LIBRARIES = []
#
#if os.name == 'posix':
#    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!search libraries")
#    for search_path in SYMBOL_SEARCH_PATH_POSIX:
#        if os.path.exists(search_path):
#            print(f"add library path: {search_path}")
#            SYMBOL_LIBRARIES.append(search_path)
#else:
#    sys.exit(f'OS {os.name} not supported!')


#from .Spice import Spice


def load_schema(filename: str):
    schema = Schema()
    parser = ParserV6()
    parser.schema(schema, filename)
    return schema

def spice_path(paths: List[str]):
    return load_spice_models(paths)

## The Scons bindings
def scons_schema(target, source, env):
    schema = load_schema(source[0].abspath)
    plot(schema, target[0].abspath, border=True)

#    files = get_kicad_files(source[0].abspath)
#    conf_file = "%s/kibot_schema.yaml" % Path(source[0].path).parent
#    create_schema_config(env, conf_file)
#    kibot = 'kibot -q -c kibot_schema.yaml -b "%s" -e "%s" -s all pdf_sch_print' % (files[1], files[0])
#    env.Execute(kibot, chdir=source[0].get_dir())
#    os.rename("%s/%s-schematic.pdf" % (source[0].get_dir(), get_kicad_name(source[0].path)), target[0].abspath)
#    os.remove(conf_file)
    return None


def generate(env):

#    env.SetDefault(KICAD_CONTEXT={})
#    env.SetDefault(KICAD_ENVIRONMENT_VARS={})
#    env.SetDefault(KICAD_TEMPLATE_SEARCHPATH=[])

#    kiscan = SCons.Script.Scanner(function = kicad_scan, skeys = ['.pro'])
#    env['BUILDERS']['preflight'] = SCons.Builder.Builder(action=kibot_preflight, source_scanner = kiscan)
    env['BUILDERS']['schema'] = SCons.Builder.Builder(action=scons_schema)
#    env['BUILDERS']['pcb'] = SCons.Builder.Builder(action=kibot_pcb, source_scanner = kiscan)
#    env['BUILDERS']['gerbers'] = SCons.Builder.Builder(action=kibot_gerbers, source_scanner = kiscan)
#    env['BUILDERS']['bom'] = SCons.Builder.Builder(action=kibot_bom, source_scanner = kiscan)
#    env['BUILDERS']['reports'] = SCons.Builder.Builder(action=kibot_combine_reports)
#    env['BUILDERS']['report2xunit'] = SCons.Builder.Builder(action=xunit)
