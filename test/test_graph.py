import unittest
import os
import sys

from rdflib import RDF,OWL
sys.path.insert(0, os.path.join(".."))

from converters.instance import convert as i_convert
from converters.model import convert as m_convert
from utility.nv_identifiers import identifiers

curr_dir = os.path.dirname(os.path.realpath(__file__))
model_fn = os.path.join(curr_dir,"..","utility","nv_model.xml")

class TestModelGraph(unittest.TestCase):
    def setUp(self):
        self.mg = m_convert(model_fn)

    def tearDown(self):
        pass

    def test_labels(self):
        for n,v,k,e in self.mg.edges(data=True,keys=True):
            edge_label = e["display_name"]
            self.assertIn(edge_label,k)

    def test_search(self):
        all_edges = self.mg.edges(data=True,keys=True)
        res = list(self.mg.search((None,None,None)))
        self.assertEqual(len(res),len(all_edges))
        for n,v,k,e in all_edges:
            n_data = self.mg.nodes[n]
            v_data = self.mg.nodes[v]
            expected_res_val = ([n,n_data],[v,v_data],k)
            self.assertIn(expected_res_val,res)



class TestNVGraph(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        for filename in os.listdir("."):
            if filename.endswith(".json"):
                os.remove(filename)

    def _graph_element_check(self,graph):
        node_id_map = {}
        for n,v,e in graph.edges(keys=True):
            n_data = graph.nodes[n]
            v_data = graph.nodes[v]
            if n in node_id_map.keys():
                self.assertEqual(node_id_map[n],n_data["key"])
            else:
                node_id_map[n] = n_data["key"]
            if v in node_id_map.keys():
                self.assertEqual(node_id_map[v],v_data["key"])
            else:
                node_id_map[v] = v_data["key"]

    def test_read_write(self):
        self.fail("Not-Updated")
        filename = os.path.join(curr_dir,"files","0x87.xml")
        nv_file = "nv_design.json"
        graph = i_convert(filename)
        graph.save(nv_file)
        reload_graph = i_convert(nv_file)
        orig_list = list(graph.edges(data=True,keys=True))
        reload_list = list(reload_graph.edges(data=True,keys=True))            
        g_diff = diff(orig_list,reload_list)
        self.assertEqual(len(g_diff), 0)

    def test_search(self):
        self.fail("Not-Updated")
        filename = os.path.join(curr_dir,"files","0xF6.xml")
        graph = i_convert(filename)
        results = graph.search((None,identifiers.predicates.rdf_type,identifiers.objects.entity))
        self.assertGreater(len(results),0)
        for n,v,e in results:
            n_id,n_data = n
            v_id,v_data = v
            g_n_data = graph.nodes[n_id]
            g_v_data = graph.nodes[v_id]
            self.assertEqual(n_data,g_n_data)
            self.assertEqual(v_data,g_v_data)
            self.assertEqual(e, identifiers.predicates.rdf_type)
            self.assertEqual(v[1]["key"], identifiers.objects.entity)
        results = graph.search((None,None,None))
        self.assertEqual(len(results),len(graph.edges))
        for n,v,e in results:
            n_id,n_data = n
            g_n_data = graph.nodes[n_id]
            self.assertEqual(n_data,g_n_data)
            v_id,v_data = v
            g_v_data = graph.nodes[v_id]
            self.assertEqual(v_data,g_v_data)

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
