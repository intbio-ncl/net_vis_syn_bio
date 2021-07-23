import unittest
import os
import sys
from random import sample

sys.path.insert(0, os.path.join(".."))

from builder.builder import NVBuilder
from graph.graph import NVGraph
from utility.nv_identifiers import identifiers

curr_dir = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(curr_dir,"files","nor_gate.xml")



class TestViewBuilder(unittest.TestCase):
    def setUp(self):
        self.vb = NVBuilder(test_file)._view_h

    def tearDown(self):
        None

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

    def test_pruned(self):
        graph = self.vb.pruned()

    def test_heirarchy(self):
        graph = self.vb.heirarchy()
        for n,v,k,e in graph.edges(keys=True,data=True):
            n_data = graph.nodes[n]
            v_data = graph.nodes[v]
            self.assertEqual(k,identifiers.predicates.contains)
            self.assertEqual(n_data["type"],"URI")
            self.assertEqual(v_data["type"],"URI")
            self.assertEqual(self.vb._builder.get_rdf_type(n)[1]["key"],identifiers.objects.entity)
            self.assertEqual(self.vb._builder.get_rdf_type(v)[1]["key"],identifiers.objects.entity)
            n_entities = self.vb._builder.get_entities(n)
            self.assertIn([v,v_data],n_entities)
        self._graph_element_check(graph)


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


class TestBuilder(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        None

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

    def test_sub_tree(self):
        rand_sample_num = 20
        filename = os.path.join(curr_dir,"files","all_or_nothing.xml")
        graph = NVBuilder(filename)

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

    def test_get_tree(self):
        filename = os.path.join(curr_dir,"files","all_or_nothing.xml")
        builder = NVBuilder(filename)
        graph = builder._graph
        builder.set_tree_mode()
        tree_graph = builder.view

        self.assertIsInstance(tree_graph,NVGraph)
        self._graph_element_check(tree_graph)
        self.assertEqual(len(graph.edges),len(tree_graph.edges))
        self.assertNotEqual(len(graph.nodes),len(tree_graph.nodes))
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
        g_search = graph.search((None,identifiers.predicates.rdf_type,identifiers.objects.entity))
        for n,v,e in g_search:
            n_id,n_data = n
            v_id,v_data = v
            t_n_data = tree_graph.nodes[n_id]
            t_v_data = tree_graph.nodes[v_id]
            self.assertEqual(n_data,t_n_data)
            self.assertEqual(v_data,t_v_data)

            t_search = tree_graph.search((n_id,None,None))
            for n1,v1,e1 in t_search:
                self.assertEqual(n1,n)


if __name__ == '__main__':
    unittest.main()
