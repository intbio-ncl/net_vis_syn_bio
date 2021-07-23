import unittest
import os
import sys

sys.path.insert(0, os.path.join(".."))

from visual.visualiser import NVisualiser
curr_dir = os.path.dirname(os.path.realpath(__file__))

class TestPresets(unittest.TestCase):
    def setUp(self):
        filename = os.path.join(curr_dir,"files","nor_gate.xml")
        self.visualiser = NVisualiser(filename)

    def tearDown(self):
        None

    def test_pruned(self):
        graph = self.vb.pruned()

    def test_heirarchy(self):
        self.visualiser.set_heirarchy_preset()
        self.visualiser.build()


    def test_components(self):
        graph = self.vb.components()

    def test_interaction_verbose(self):
        graph = self.vb.interaction_verbose()

    def test_interaction(self):
        graph = self.vb.interaction()

    def test_interaction_genetic(self):
        graph = self.vb.interaction_genetic()

    def test_ppi(self):
        graph = self.vb.ppi()

    def test_module(self):
        graph = self.vb.module()

    def test_maps(self):
        graph = self.vb.maps()

class TestVisual(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        None


    
if __name__ == '__main__':
    unittest.main()
