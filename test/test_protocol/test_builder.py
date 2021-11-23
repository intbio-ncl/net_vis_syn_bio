from re import L
import unittest
import os
import sys

from rdflib import URIRef

sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))

from builder.protocol import ProtocolBuilder

curr_dir = os.path.dirname(os.path.realpath(__file__))
instance_file = os.path.join(curr_dir,"..","files","1_clip.ot2.py")
model_file = os.path.join(curr_dir,"..","..","utility","nv_protocol.xml")

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.builder = ProtocolBuilder(model_file,instance_file)
        self.graph = self.builder._graph

    def tearDown(self):
        pass

    def test_get_protocol(self):
        protocol = self.builder.get_protocol()[0]
        protocol_uri = protocol[0][1]["key"]
        protocol_type = protocol[1][1]["key"]
        self.assertEqual(protocol_uri,URIRef("http://www.nv_ontology.org/ot2_layer_mixed"))
        self.assertEqual(protocol_type,URIRef("http://www.nv_ontology.org/Protocol"))
    
class TestViews(unittest.TestCase):
    def setUp(self):
        self.builder = ProtocolBuilder(model_file,instance_file)
        self.model = self.builder._model_graph

    def tearDown(self):
        pass

    def test_flow(self):
        self.builder.set_flow_view()
        graph = self.builder.view

    def test_heirarchy(self):
        self.builder.set_heirarchy_view()
        graph = self.builder.view

    def test_process_verbose(self):
        self.builder.set_process_verbose_view()
        graph = self.builder.view
        for n,v,e in graph.edges(keys=True):
            n_data = graph.nodes[n]
            v_data = graph.nodes[v]

    def test_process_implicit(self):
        self.builder.set_process_implicit_view()
        graph = self.builder.view

    def test_process_explicit(self):
        self.builder.set_process_explicit_view()
        graph = self.builder.view

class TestModes(unittest.TestCase):
        def setUp(self):
            self.builder = ProtocolBuilder(model_file,instance_file)

        def tearDown(self):
            pass
        




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

def _diff(list1,list2):
    diff = []
    for n,v,e in list1:
        for n1,v1,e1 in list2:
            if n == n1 and v == v1 and e == e1:
                break
        else:
            diff.append((n,v,e,k))
    return diff


if __name__ == '__main__':
    unittest.main()
