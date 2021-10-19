import unittest
import os
import sys

from rdflib import RDF,OWL
sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))

from converters.model import convert as m_convert
from converters.design import convert as i_convert

curr_dir = os.path.dirname(os.path.realpath(__file__))
test_fn = test_dir = os.path.join(curr_dir,"..","files","nor_gate.xml")
model_fn = os.path.join(curr_dir,"..","..","utility","nv_design.xml")

class TestDesignGraph(unittest.TestCase):

    def setUp(self):
        self.graph = i_convert(m_convert(model_fn),test_fn)

    def tearDown(self):
        for filename in os.listdir("."):
            if filename.endswith(".json"):
                os.remove(filename)

    def test_labels(self):
        for n,v,k,e in self.graph.edges(data=True,keys=True):
            edge_label = e["display_name"]
            self.assertIn(edge_label,k)

    def test_search(self):
        all_edges = self.graph.edges(data=True,keys=True)
        res = list(self.graph.search((None,None,None)))
        self.assertEqual(len(res),len(all_edges))
        for n,v,k,e in all_edges:
            n_data = self.graph.nodes[n]
            v_data = self.graph.nodes[v]
            expected_res_val = ([n,n_data],[v,v_data],k)
            self.assertIn(expected_res_val,res)

    def test_get_rdf_type(self):
        for n,v,e in self.graph.search((None,RDF.type,None)):
            n,n_data = n
            self.assertEqual(self.graph.get_rdf_type(n),v)

def diff(list1,list2):
    diff = []
    for n,v,e,k in list1:
        for n1,v1,e1,k1 in list2:
            if n == n1 and v == v1 and e == e1 and k == k1:
                break
        else:
            diff.append((n,v,e,k))
    return diff

if __name__ == '__main__':
    unittest.main()
