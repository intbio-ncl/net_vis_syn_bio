import unittest
import os
import sys

sys.path.insert(0, os.path.join("..","..","..",".."))
sys.path.insert(0, os.path.join("..","..",".."))
sys.path.insert(0, os.path.join("..",".."))

from converters.converter import convert
curr_dir = os.path.dirname(os.path.realpath(__file__))

class TestConvert(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        None

    def test_convert(self):
        filename = os.path.join(curr_dir,"files","test_convert2.xml")
        graph = convert(filename,"sbol")
        for n,v,k,e in graph.edges(keys=True,data=True):
            print(n,v,k,e)


if __name__ == '__main__':
    unittest.main()
