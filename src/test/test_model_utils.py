from os import wait
import sys
import unittest
import numpy as np
from pprint import pprint
sys.path.append("src")
sys.path.append("../src")

from nukleus.Library import Library
from nukleus.ModelSchema import Symbol, Property, TextEffects
from nukleus.transform import isUnit, totuple, pinPosition, pinByPositions, placeFields


class TestUtilsPlaceFields(unittest.TestCase):
    def test_is_totuple(self):
        self.assertEqual(((0, 0), (0, 0)), totuple(np.array([[0, 0], [0, 0]])))
        self.assertEqual((0, 0), totuple(np.array([0, 0])))

    def test_is_unit(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R')
        self.assertFalse(isUnit(lib_sym, 1))
        self.assertTrue(isUnit(lib_sym.units[0], 1))
        self.assertTrue(isUnit(lib_sym.units[1], 1))

    def test_is_unit_opamp(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        self.assertFalse(isUnit(lib_sym, 1))
        self.assertTrue(isUnit(lib_sym.units[0], 1))
        self.assertFalse(isUnit(lib_sym.units[1], 1))
        self.assertFalse(isUnit(lib_sym.units[2], 1))

    def test_get_pins_by_pos(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R')
        symbol = Symbol(properties=[Property(key="Reverence", value="R1", text_effects=TextEffects(hidden=False))], library_identifier="Device:R",
                            library_symbol=lib_sym)
        pos = pinByPositions(symbol)
        self.assertEqual([0,1,0,1], [len(x) for x in pos.values()])
        self.assertEqual('1', pos['north'][0].number[0])
        self.assertEqual('2', pos['south'][0].number[0])

    def test_get_pins_by_pos_rotate(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R')
        symbol = Symbol(properties=[Property(key="Reverence", value="R1", text_effects=TextEffects(hidden=False))], library_identifier="Device:R",
                            library_symbol=lib_sym)
        symbol.angle = 270
        pos = pinByPositions(symbol)
        self.assertEqual([1,0,1,0], [len(x) for x in pos.values()])
        self.assertEqual('2', pos['west'][0].number[0])
        self.assertEqual('1', pos['east'][0].number[0])

    def test_get_pot_pins_by_pos(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R_Potentiometer')
        symbol = Symbol(properties=[Property(key="Reverence", value="RV1", text_effects=TextEffects(hidden=False))], library_identifier="Device:R_Potentiometer",
                            library_symbol=lib_sym)
        pos = pinByPositions(symbol)
        self.assertEqual([0,1,1,1], [len(x) for x in pos.values()])
        self.assertEqual('1', pos['north'][0].number[0])
        self.assertEqual('2', pos['east'][0].number[0])
        self.assertEqual('3', pos['south'][0].number[0])

    def test_get_transistor_pins_by_pos(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Transistor_BJT:BC547')
        symbol = Symbol(properties=[Property(key="Reverence", value="Q1", text_effects=TextEffects(hidden=False))], library_identifier="Transistor_BJT:BC547",
                            library_symbol=lib_sym)
        pos = pinByPositions(symbol)
        self.assertEqual([1,1,0,1], [len(x) for x in pos.values()])
        self.assertEqual('1', pos['north'][0].number[0])
        self.assertEqual('2', pos['west'][0].number[0])
        self.assertEqual('3', pos['south'][0].number[0])

    def test_get_transistor_pins_by_pos_mirror(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Transistor_BJT:BC547')
        symbol = Symbol(properties=[Property(key="Reverence", value="Q1", text_effects=TextEffects(hidden=False))], library_identifier="Transistor_BJT:BC547",
                            library_symbol=lib_sym)
        symbol.mirror = 'y'
        pos = pinByPositions(symbol)
        self.assertEqual([0,1,1,1], [len(x) for x in pos.values()])
        self.assertEqual('1', pos['north'][0].number[0])
        self.assertEqual('2', pos['east'][0].number[0])
        self.assertEqual('3', pos['south'][0].number[0])

    def test_get_pin_pos(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R')
        symbol = Symbol(properties=[Property(key='Reference', value='R1', text_effects=TextEffects(hidden=False))],
                        library_identifier="Device:R",
                        library_symbol=lib_sym)
        pos = pinPosition(symbol)
        self.assertEqual([0,1,0,1], pos)

    def test_get_pin_pos_rotate(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Device:R')
        symbol = Symbol(properties=[Property(key="Reverence", value="R1", text_effects=TextEffects(hidden=False))], library_identifier="Device:R",
                            library_symbol=lib_sym)
        symbol.angle = 90
        pos = pinPosition(symbol)
        self.assertEqual([1,0,1,0], pos)

    def test_get_pin_pos_opamp(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        symbol = Symbol(properties=[Property(key="Reverence", value="U1", text_effects=TextEffects(hidden=False))], library_identifier="Amplifier_Operational:TL072",
                            library_symbol=lib_sym, unit=1)
        pos = pinPosition(symbol)
        self.assertEqual([2,0,1,0], pos)

    def test_get_pin_pos_opamp_rotate(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        symbol = Symbol(properties=[Property(key="Reverence", value="U1", text_effects=TextEffects(hidden=False))], library_identifier="Amplifier_Operational:TL072",
                            library_symbol=lib_sym, unit=1)
        symbol.angle = 180
        pos = pinPosition(symbol)
        self.assertEqual([1,0,2,0], pos)

    def test_get_pin_pos_opamp_mirror_x(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        symbol = Symbol(properties=[Property(key="Reverence", value="U1", text_effects=TextEffects(hidden=False))], library_identifier="Amplifier_Operational:TL072",
                            library_symbol=lib_sym, unit=1)
        symbol.mirror = 'x'
        pos = pinPosition(symbol)
        self.assertEqual([2,0,1,0], pos)

    def test_get_pin_pos_opamp_mirror_y(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        symbol = Symbol(properties=[Property(key="Reverence", value="U1", text_effects=TextEffects(hidden=False))], library_identifier="Amplifier_Operational:TL072",
                            library_symbol=lib_sym, unit=1)
        symbol.mirror = 'y'
        pos = pinPosition(symbol)
        self.assertEqual([1,0,2,0], pos)

    def test_get_pin_pos_power(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('power:+15V')
        symbol = Symbol(properties=[Property(key="Reverence", value="+15V", text_effects=TextEffects(hidden=False))], library_identifier="power:+15V",
                            library_symbol=lib_sym)
        pos = pinPosition(symbol)
        self.assertEqual([0,1,0,0], pos)

    def test_get_pin_pos_gnd(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('power:GND')
        symbol = Symbol(properties=[Property(key="Reverence", value="GND", text_effects=TextEffects(hidden=False))], library_identifier="power:GND",
                            library_symbol=lib_sym)
        pos = pinPosition(symbol)
        self.assertEqual([0,0,0,1], pos)
# TODO
#    def test_place_opamp(self):
#        lib = Library(['samples/files/symbols/'])
#        lib_sym = lib.get('Amplifier_Operational:TL072')
#        symbol = Symbol(properties=[Property(key="Reverence", value="U1", text_effects=TextEffects(hidden=False))], library_identifier="Amplifier_Operational:TL072",
#                            library_symbol=lib_sym, unit=1)
#        placeFields(symbol)
#        self.assertEqual((0, -8.36), symbol.properties[0].pos)
#        self.assertEqual((0, -6.359999999999999), symbol.properties[1].pos)
#
#    def test_place_resistor(self):
#        lib = Library(['samples/files/symbols/'])
#        lib_sym = lib.get('Device:R')
#        symbol = Symbol(properties=[Property(key="Reverence", value="R1", text_effects=TextEffects(hidden=False))], library_identifier="Device:R",
#                            library_symbol=lib_sym)
#        placeFields(symbol)
#        self.assertEqual((1.778, -1.0), symbol.properties[0].pos)
#        self.assertEqual((1.778, 1.0), symbol.properties[1].pos)
#
#    def test_place_resistor_rotate(self):
#        lib = Library(['samples/files/symbols/'])
#        lib_sym = lib.get('Device:R')
#        symbol = Symbol(properties=[Property(key="Reverence", value="R1", text_effects=TextEffects(hidden=False))], library_identifier="Device:R",
#                            library_symbol=lib_sym)
#        symbol.angle = 90
#        placeFields(symbol)
#        self.assertEqual((0, -4.296), symbol.properties[0].pos)
#        self.assertEqual((0, -2.2960000000000003), symbol.properties[1].pos)

    def test_place_single_pin_item(self):
        lib = Library(['samples/files/symbols/'])
        lib_sym = lib.get('power:+15V')
        symbol = Symbol(pos=(100, 100), properties=[Property(key="Reverence", value="+15V",
                        text_effects=TextEffects(hidden=False))],
                        library_identifier="power:+15V",
                        library_symbol=lib_sym)
        placeFields(symbol)
        self.assertEqual((100.0, 96.17999999999999), symbol.properties[0].pos)
