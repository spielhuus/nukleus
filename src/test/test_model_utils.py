import sys
import unittest

sys.path.append("src")
sys.path.append("../src")

from nukleus.Library import Library
from nukleus.model.Symbol import Symbol
from nukleus.model.Utils import pinPosition, placeFields, is_unit


class TestUtilsPlaceFields(unittest.TestCase):
    def test_is_unit(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R')
        self.assertFalse(is_unit(lib_sym, 1))
        self.assertTrue(is_unit(lib_sym.units[0], 1))
        self.assertTrue(is_unit(lib_sym.units[1], 1))

    def test_is_unit_opamp(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        self.assertFalse(is_unit(lib_sym, 1))
        self.assertTrue(is_unit(lib_sym.units[0], 1))
        self.assertFalse(is_unit(lib_sym.units[1], 1))
        self.assertFalse(is_unit(lib_sym.units[2], 1))

    def test_get_pin_pos(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R')
        symbol = Symbol.new(ref="R1", lib_name="Device:R",
                            library_symbol=lib_sym)
        pos = pinPosition(symbol)
        self.assertEqual([0,1,0,1], pos)

    def test_get_pin_pos_rotate(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R')
        symbol = Symbol.new(ref="R1", lib_name="Device:R",
                            library_symbol=lib_sym)
        symbol.angle = 90
        pos = pinPosition(symbol)
        self.assertEqual([1,0,1,0], pos)

    def test_get_pin_pos_opamp(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        symbol = Symbol.new(ref="U1", lib_name="Amplifier_Operational:TL072",
                            library_symbol=lib_sym, unit=1)
        pos = pinPosition(symbol)
        self.assertEqual([2,0,1,0], pos)

    def test_get_pin_pos_opamp_rotate(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        symbol = Symbol.new(ref="U1", lib_name="Amplifier_Operational:TL072",
                            library_symbol=lib_sym, unit=1)
        symbol.angle = 180
        pos = pinPosition(symbol)
        self.assertEqual([1,0,2,0], pos)

    def test_get_pin_pos_opamp_mirror_x(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        symbol = Symbol.new(ref="U1", lib_name="Amplifier_Operational:TL072",
                            library_symbol=lib_sym, unit=1)
        symbol.mirror = 'x'
        pos = pinPosition(symbol)
        self.assertEqual([1,0,2,0], pos)

    def test_get_pin_pos_opamp_mirror_y(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        symbol = Symbol.new(ref="U1", lib_name="Amplifier_Operational:TL072",
                            library_symbol=lib_sym, unit=1)
        symbol.mirror = 'y'
        pos = pinPosition(symbol)
        self.assertEqual([2,0,1,0], pos)

    def test_get_pin_pos_power(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('power:+15V')
        symbol = Symbol.new(ref="+15V", lib_name="power:+15V",
                            library_symbol=lib_sym)
        pos = pinPosition(symbol)
        self.assertEqual([0,1,0,0], pos)

    def test_get_pin_pos_gnd(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('power:GND')
        symbol = Symbol.new(ref="GND", lib_name="power:GND",
                            library_symbol=lib_sym)
        pos = pinPosition(symbol)
        self.assertEqual([0,0,0,1], pos)

    def test_place_opamp(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        symbol = Symbol.new(ref="U1", lib_name="Amplifier_Operational:TL072",
                            library_symbol=lib_sym, unit=1)
        placeFields(symbol)
        self.assertEqual((0, -7.8420000000000005), symbol.properties[0].pos)
        self.assertEqual((0, -5.8420000000000005), symbol.properties[1].pos)

    def test_place_resistor(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R')
        symbol = Symbol.new(ref="R1", lib_name="Device:R",
                            library_symbol=lib_sym)
        placeFields(symbol)
        self.assertEqual((1.778, -1.0), symbol.properties[0].pos)
        self.assertEqual((1.778, 1.0), symbol.properties[1].pos)

    def test_place_resistor_rotate(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R')
        symbol = Symbol.new(ref="R1", lib_name="Device:R",
                            library_symbol=lib_sym)
        symbol.angle = 90
        placeFields(symbol)
        self.assertEqual((0, -3.778), symbol.properties[0].pos)
        self.assertEqual((0, -1.778), symbol.properties[1].pos)

    def test_place_single_pin_item(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('power:+15V')
        symbol = Symbol.new(ref="+15V", lib_name="power:+15V",
                        library_symbol=lib_sym)
        placeFields(symbol)
        self.assertEqual((0.0, -3.81), symbol.properties[0].pos)
