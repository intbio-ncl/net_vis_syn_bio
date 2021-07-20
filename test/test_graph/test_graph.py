import unittest
import os
import sys
from random import sample

import rdflib
import networkx as nx
sys.path.insert(0, os.path.join("..","..","..",".."))
sys.path.insert(0, os.path.join("..","..",".."))
sys.path.insert(0, os.path.join("..",".."))
curr_dir = os.path.dirname(os.path.realpath(__file__))
from graph.graph import NVGraph
from utility.nv_identifiers import identifiers

class TestNVGraph(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        None

    def _graph_element_check(self,graph):
        node_id_map = {}
        for n,v,e in graph.edges:
            n_data = graph.nodes[n]
            v_data = graph.nodes[v]
            self.assertEqual(e[0],n_data["key"])
            self.assertEqual(e[2],v_data["key"])
            if n in node_id_map.keys():
                self.assertEqual(node_id_map[n],n_data["key"])
            else:
                node_id_map[n] = n_data["key"]
            if v in node_id_map.keys():
                self.assertEqual(node_id_map[v],v_data["key"])
            else:
                node_id_map[v] = v_data["key"]

    def test_read_write(self):
        pass

    def test_sub_tree(self):
        rand_sample_num = 20
        filename = os.path.join(curr_dir,"files","test_sub_tree.xml")
        graph = NVGraph(filename)

        sub_edges = sample(list(graph.edges),rand_sample_num)
        node_attrs = {}
        for n,v,e in sub_edges:
            node_attrs[n] = graph.nodes[n]
            node_attrs[v] = graph.nodes[v]
            
        sub_graph = graph.sub_graph(sub_edges,node_attrs)
        self.assertIsInstance(sub_graph,NVGraph)
        self.assertEqual(len(sub_graph.edges),rand_sample_num)
        graph_triples = [e for n,v,e in graph.edges]
        sub_triples = [e for n,v,e in sub_graph.edges]
        [self.assertIn(sub_triple,graph_triples) for sub_triple in sub_triples]
        self.assertCountEqual(sub_edges,sub_graph.edges)
        self._graph_element_check(sub_graph)

        for n,v,e in sub_graph.edges:
            n_data = sub_graph.nodes[n]
            n_data_orig = graph.nodes[n]
            self.assertTrue(n_data == n_data_orig)
            v_data = sub_graph.nodes[v]
            v_data_orig = graph.nodes[v]
            self.assertTrue(v_data == v_data_orig)

    def test_search(self):
        filename = os.path.join(curr_dir,"files","test_search.xml")
        graph = NVGraph(filename)
        results = graph.search((None,identifiers.predicates.rdf_type,identifiers.objects.entity))
        self.assertGreater(len(results),0)
        for n,v,e in results:
            n_id,n_data = n
            g_n_data = graph.nodes[n_id]
            self.assertEqual(n_data,g_n_data)

            v_id,v_data = v
            g_v_data = graph.nodes[v_id]
            self.assertEqual(v_data,g_v_data)
            self.assertEqual(e[1], identifiers.predicates.rdf_type)
            self.assertEqual(e[2], identifiers.objects.component_definition)

        results = graph.search((None,None,None))
        self.assertEqual(len(results),len(graph.edges))
        for n,v,e in results:
            n_id,n_data = n
            g_n_data = graph.nodes[n_id]
            self.assertEqual(n_data,g_n_data)
            v_id,v_data = v
            g_v_data = graph.nodes[v_id]
            self.assertEqual(v_data,g_v_data)
        

    def test_get_tree(self):
        filename = os.path.join(curr_dir,"files","test_rdf_to_networkx.xml")
        graph = NVGraph(filename)
        tree_graph = graph.get_tree()
        self.assertIsInstance(tree_graph,NVGraph)
        self._graph_element_check(tree_graph)
        for n,v,e in tree_graph.edges:
            n_data = tree_graph.nodes[n]
            v_data = tree_graph.nodes[v]
            try:
                orig_n_data = graph.nodes[n]
                self.assertEqual(n_data,orig_n_data)
            except KeyError:
                orig_node_id = [x for x,y in graph.nodes(data=True) if y['key'] == n_data["key"]]
                self.assertEqual(len(orig_node_id),1)
                orig_node_id = orig_node_id[0]
                self.assertEqual(tree_graph.nodes[orig_node_id],n_data)
            try:
                orig_v_data = graph.nodes[v]
                self.assertEqual(v_data,orig_v_data)
            except KeyError:
                orig_node_id = [x for x,y in graph.nodes(data=True) if y['key'] == v_data["key"]]
                self.assertEqual(len(orig_node_id),1)
                orig_node_id = orig_node_id[0]
                self.assertEqual(tree_graph.nodes[orig_node_id],v_data)


if __name__ == '__main__':
    unittest.main()
