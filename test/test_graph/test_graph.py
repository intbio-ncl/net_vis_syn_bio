from operator import sub
import unittest
import os
import sys
from random import sample
from networkx.readwrite.json_graph import tree

import rdflib
import networkx as nx
sys.path.insert(0, os.path.join("..","..","..",".."))
sys.path.insert(0, os.path.join("..","..",".."))
sys.path.insert(0, os.path.join("..",".."))
curr_dir = os.path.dirname(os.path.realpath(__file__))
from converters.converter import convert
from graph.graph import NVGraph
from utility.nv_identifiers import identifiers

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
        filename = os.path.join(curr_dir,"files","test_graph.xml")
        nv_file = "nv_design.json"
        graph = convert(filename)
        graph.save(nv_file)
        reload_graph = convert(nv_file)
        orig_list = list(graph.edges(data=True,keys=True))
        reload_list = list(reload_graph.edges(data=True,keys=True))            
        g_diff = diff(orig_list,reload_list)
        self.assertEqual(len(g_diff), 0)

    def test_search(self):
        filename = os.path.join(curr_dir,"files","test_graph.xml")
        graph = convert(filename)
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

    def test_sub_tree(self):
        rand_sample_num = 20
        filename = os.path.join(curr_dir,"files","test_graph.xml")
        graph = convert(filename)

        sub_edges = sample(list(graph.edges(keys=True,data=True)),rand_sample_num)
        node_attrs = {}
        for n,v,k,e in sub_edges:
            node_attrs[n] = graph.nodes[n]
            node_attrs[v] = graph.nodes[v]
            
        sub_graph = graph.sub_graph(sub_edges,node_attrs)
        self.assertIsInstance(sub_graph,NVGraph)
        self.assertEqual(len(sub_graph.edges),rand_sample_num)
        graph_triples = [e for n,v,e in graph.edges]
        sub_triples = [e for n,v,e in sub_graph.edges]
        [self.assertIn(sub_triple,graph_triples) for sub_triple in sub_triples]
        self.assertCountEqual(sub_edges,sub_graph.edges(keys=True,data=True))
        self._graph_element_check(sub_graph)

        for n,v,k,e in sub_graph.edges(data=True,keys=True):
            n_data = sub_graph.nodes[n]
            n_data_orig = graph.nodes[n]
            self.assertTrue(n_data == n_data_orig)
            v_data = sub_graph.nodes[v]
            v_data_orig = graph.nodes[v]
            self.assertTrue(v_data == v_data_orig)
            orig_edge_data = graph.edges[n,v,k]
            self.assertEqual(orig_edge_data,e)
            

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
