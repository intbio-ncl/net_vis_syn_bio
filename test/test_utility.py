import unittest
import os
import sys

from rdflib import RDF,OWL
sys.path.insert(0, os.path.join(".."))

from converters.model import convert as m_convert
from utility.identifiers import produce_identifiers
curr_dir = os.path.dirname(os.path.realpath(__file__))
model_fn = os.path.join(curr_dir,"..","utility","nv_model.xml")

class TestUtility(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_produce_identifiers(self):
        graph = m_convert(model_fn)
        identifiers = produce_identifiers(graph)

        

if __name__ == '__main__':
    unittest.main()
