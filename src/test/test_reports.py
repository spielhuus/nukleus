import sys
import unittest
import io
import pprint

sys.path.append('src')
sys.path.append('..')

from nukleus.Reports import report_parser
import nukleus

DRC_STRING = """** Drc report for /home/etienne/nukleus/samples/scons/main.kicad_pcb **
** Created on 2022-03-05 15:28:44 **

** Found 8 DRC violations **
[track_dangling]: Track has unconnected end
    Local override; Severity: warning
    @(51.3080 mm, 94.4880 mm): Track [GND] on F.Cu, length 5.2500 mm
[track_dangling]: Track has unconnected end
    Local override; Severity: warning
    @(51.3080 mm, 80.2640 mm): Track [GND] on F.Cu, length 3.2919 mm
[track_dangling]: Track has unconnected end
    Local override; Severity: warning
    @(74.6760 mm, 120.9040 mm): Track [GND] on B.Cu, length 0.5480 mm
[track_dangling]: Track has unconnected end
    Local override; Severity: warning
    @(72.0545 mm, 73.6600 mm): Track [+15V] on F.Cu, length 0.5211 mm
[track_dangling]: Track has unconnected end
    Local override; Severity: warning
    @(72.8765 mm, 70.8875 mm): Track [-15V] on F.Cu, length 2.0320 mm
[track_dangling]: Track has unconnected end
    Local override; Severity: warning
    @(67.5640 mm, 76.2000 mm): Track [-15V] on F.Cu, length 1.3265 mm
[track_dangling]: Track has unconnected end
    Local override; Severity: warning
    @(53.3400 mm, 79.7560 mm): Track [+5V] on F.Cu, length 3.4290 mm
[track_dangling]: Track has unconnected end
    Local override; Severity: warning
    @(63.3425 mm, 132.9385 mm): Track [Net-(U2-Pad1)] on F.Cu, length 2.4070 mm

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **"""

class TestReports(unittest.TestCase):

    def test_parse_drc(self):
        out = {}
        report_parser(DRC_STRING, out)
        self.assertEqual(2, len(out))
        self.assertEqual(8, len(out['drc']))

#TODO
#    def test_parse_erc(self):
#        schema = nukleus.load_schema('samples/files/summe_v6/main.kicad_sch')
#        netlist = nukleus.Spice.netlist(schema)
#        erc_res = nukleus.erc(schema, netlist)
#        pprint.pprint(erc_res)
#        self.assertEqual(1, len(erc_res))
