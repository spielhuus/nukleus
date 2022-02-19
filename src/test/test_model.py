import sys
sys.path.append('src')
sys.path.append('../../src')

import unittest

from sys import path
path.append('src')

from nukleus import Schema, load_schema
from nukleus.Library import Library
from nukleus.model import Symbol, Pin, PinList, LibrarySymbol

#class TestModel(unittest.TestCase):
#    def test_get_pins(self):
#        lib = Library(['samples/files/symbols/'])
#        lib_sym = lib.get('Device:R')
#        symbol = Symbol.new("1", "Device:R", lib_sym)
#
#        syms = symbol.getPins()
#        self.assertEqual(2, len(syms))
#        
#    def test_get_pins_power(self):
#        lib = Library(['samples/files/symbols'])
#        lib_sym = lib.get('power:-15V')
#        symbol = Symbol.new("1", "-15V", lib_sym)
#
#        syms = symbol.getPins()
#        self.assertEqual(1, len(syms))
#        
#
#class TestPinList(unittest.TestCase):
#    def test_pin_list(self):
#        list = PinList()
#        symbol = Symbol.new('ref', 'Device:R', LibrarySymbol.new(), 1)
#        list.append(symbol, Pin.new('1', 'name1'))
#        list.append(symbol, Pin.new('2', 'name2'))
#        list.append(symbol, Pin.new('3', 'name3'))
#
#        self.assertEqual(3, len(list))
#        self.assertTrue(isinstance(list['1'], Pin))
#        self.assertEqual('name1', list['1'].name[0])
#
#    def test_pin_iter(self):
#        list = PinList()
#        symbol = Symbol.new('ref', 'Device:R', LibrarySymbol.new(), 1)
#        list.append(symbol, Pin.new('1', 'name1'))
#        list.append(symbol, Pin.new('2', 'name2'))
#        list.append(symbol, Pin.new('3', 'name3'))
#        
#        res = ''
#        for pin in list:
#            res += pin.name[0]
#        
#        self.assertEqual('name1name2name3', res)
#
#class TestGetPin(unittest.TestCase):
#    def test_pin_list(self):
#        schema = load_schema("samples/files/summe_v6/main.kicad_sch")
#
#        element = schema.R5[1]
#        pin = element.getPins()['1']
#
#        self.assertEqual('~', pin.name[0])
