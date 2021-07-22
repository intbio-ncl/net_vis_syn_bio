import unittest
import os
import sys

sys.path.insert(0, os.path.join("..","..","..",".."))
sys.path.insert(0, os.path.join("..","..",".."))
sys.path.insert(0, os.path.join("..",".."))

from visual.visualiser import NVisualiser
curr_dir = os.path.dirname(os.path.realpath(__file__))

class TestVisual(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        None

    def test_init(self):
        pass
    
    def test_tree_view(self):
        filename = os.path.join(curr_dir,"files","test_visual.xml")
        visualiser = NVisualiser(filename)

        visualiser.set_tree_mode()
        #visualiser.add_node_name_labels()
        #visualiser.add_edge_name_labels()
        visualiser.add_rdf_type_node_color()
        #visualiser.add_type_node_size()
        #visualiser.set_adaptive_node_shape()
        visualiser.build()


    
if __name__ == '__main__':
    unittest.main()
