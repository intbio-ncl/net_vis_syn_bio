import unittest
import os
import sys
from random import sample

from rdflib import RDF,BNode
sys.path.insert(0, os.path.join(".."))

from builder.instance import InstanceBuilder

curr_dir = os.path.dirname(os.path.realpath(__file__))
instance_file = os.path.join(curr_dir,"..","files","nor_gate.xml")

def _graph_element_check(graph):
    node_id_map = {}
    for n,v,e in graph.edges(keys=True):
        n_data = graph.nodes[n]
        v_data = graph.nodes[v]
        if n in node_id_map.keys():
            if node_id_map[n] != n_data["key"]:
                return False
        else:
            node_id_map[n] = n_data["key"]
        if v in node_id_map.keys():
            if node_id_map[v] != v_data["key"]:
                return False
        else:
            node_id_map[v] = v_data["key"]
    return True

class TestInstanceBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = InstanceBuilder(instance_file)

    def tearDown(self):
        pass

    def test_sub_tree(self):
        rand_sample_num = 20
        sub_edges = sample(list(self.builder.edges(keys=True,data=True)),rand_sample_num)
        node_attrs = {}
        for n,v,k,e in sub_edges:
            node_attrs[n] = self.builder.nodes[n]
            node_attrs[v] = self.builder.nodes[v]
            
        sub_graph = self.builder.sub_graph(sub_edges,node_attrs)
        self.assertIsInstance(sub_graph,self.builder._graph.__class__)
        self.assertEqual(len(sub_graph.edges),rand_sample_num)
        graph_triples = [e for n,v,e in self.builder.edges]
        sub_triples = [e for n,v,e in sub_graph.edges]
        [self.assertIn(sub_triple,graph_triples) for sub_triple in sub_triples]
        self.assertCountEqual(sub_edges,sub_graph.edges(keys=True,data=True))
        self.assertTrue(_graph_element_check(sub_graph))

        for n,v,k,e in sub_graph.edges(data=True,keys=True):
            n_data = sub_graph.nodes[n]
            n_data_orig = self.builder.nodes[n]
            self.assertTrue(n_data == n_data_orig)
            v_data = sub_graph.nodes[v]
            v_data_orig = self.builder.nodes[v]
            self.assertTrue(v_data == v_data_orig)
            orig_edge_data = self.builder.edges[n,v,k]
            self.assertEqual(orig_edge_data,e)

    def test_get_tree(self):
        self.builder.set_tree_mode()
        tree_graph = self.builder.view

        self.assertIsInstance(tree_graph,self.builder._graph.__class__)
        self.assertTrue(_graph_element_check(tree_graph))
        self.assertEqual(len( self.builder.edges),len(tree_graph.edges))
        self.assertNotEqual(len( self.builder.nodes),len(tree_graph.nodes))
        for n,v,e in tree_graph.edges:
            n_data = tree_graph.nodes[n]
            v_data = tree_graph.nodes[v]
            try:
                orig_n_data = self.builder.nodes[n]
                self.assertEqual(n_data,orig_n_data)
            except KeyError:
                orig_node_id = [x for x,y in self.builder.nodes(data=True) if y['key'] == n_data["key"]]
                self.assertEqual(len(orig_node_id),1)
                orig_node_id = orig_node_id[0]
                self.assertEqual(tree_graph.nodes[orig_node_id],n_data)
            try:
                orig_v_data = self.builder.nodes[v]
                self.assertEqual(v_data,orig_v_data)
            except KeyError:
                orig_node_id = [x for x,y in self.builder.nodes(data=True) if y['key'] == v_data["key"]]
                self.assertEqual(len(orig_node_id),1)
                orig_node_id = orig_node_id[0]
                self.assertEqual(tree_graph.nodes[orig_node_id],v_data)
        g_search = self.builder._graph.search((None,RDF.type,None))
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

    def test_pruned(self):
        self.builder.set_pruned_view()
        graph = self.builder.view

    def test_heirarchy(self):
        self.builder.set_heirarchy_view()
        graph = self.builder.view
        for n,v,k,e in self.builder.edges(keys=True,data=True):
            n_data = self.builder.nodes[n]
            v_data = self.builder.nodes[v]
            self.assertEqual(k,identifiers.predicates.contains)
            self.assertEqual(n_data["type"],"URI")
            self.assertEqual(v_data["type"],"URI")
            self.assertEqual(self.vb._builder.get_rdf_type(n)[1]["key"],identifiers.objects.entity)
            self.assertEqual(self.vb._builder.get_rdf_type(v)[1]["key"],identifiers.objects.entity)
            n_entities = self.builder._builder.get_entities(n)
            self.assertIn([v,v_data],n_entities)
        self._graph_element_check(graph)





if __name__ == '__main__':
    unittest.main()
