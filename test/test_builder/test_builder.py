import unittest
import os
import sys

sys.path.insert(0, os.path.join("..","..","..",".."))
sys.path.insert(0, os.path.join("..","..",".."))
sys.path.insert(0, os.path.join("..",".."))

from builder.builder import NVBuilder
from graph.graph import NVGraph
from utility.nv_identifiers import identifiers

curr_dir = os.path.dirname(os.path.realpath(__file__))

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

    def test_get_tree(self):
        filename = os.path.join(curr_dir,"files","test_builder.xml")
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
