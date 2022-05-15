#import sys
#import unittest
#
#sys.path.append("src")
#sys.path.append("..")
#
#from nukleus.model.FootprintAttributes import FootprintAttributes
#from nukleus.SexpParser import load_tree
#
#INPUT_STRING_1 = """  (attr through_hole)"""
#INPUT_STRING_2 = """  (attr exclude_from_pos_files)"""
#
#
#class TestFootprintAttributes(unittest.TestCase):
#    def test_parse_attributes_1(self):
#        sexp_str = load_tree(INPUT_STRING_1)
#        attribute = FootprintAttributes.parse(sexp_str)
#
#        self.assertEqual('through_hole', attribute.attribute_type)
#
#    def test_parse_attributes_2(self):
#        sexp_str = load_tree(INPUT_STRING_2)
#        attribute = FootprintAttributes.parse(sexp_str)
#
#        self.assertTrue(attribute.exclude_from_pos_files)
#
#    def test_layers_sexp(self):
#        sexp_str = load_tree(INPUT_STRING_1)
#        layers = FootprintAttributes.parse(sexp_str)
#        self.assertEqual(INPUT_STRING_1, layers.sexp(indent=1))
