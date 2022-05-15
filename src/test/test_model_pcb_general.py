#import sys
#import unittest
#
#from nukleus.model.General import General
#from nukleus.SexpParser import load_tree
#
#sys.path.append('src')
#sys.path.append('..')
#
#
#INPUT_STRINGG = """  (general
#    (thickness 1.6)
#    (drawings 4)
#    (tracks 253)
#    (zones 0)
#    (modules 37)
#    (nets 25)
#  )"""
#
#
#class TestGeneral(unittest.TestCase):
#    def test_parse_general(self):
#        sexp_str = load_tree(INPUT_STRINGG)
#        general = General.parse(sexp_str)
#
#        self.assertEqual(6, len(general.values))
#        self.assertEqual('1.6', general.values['thickness'])
#        self.assertEqual('4', general.values['drawings'])
