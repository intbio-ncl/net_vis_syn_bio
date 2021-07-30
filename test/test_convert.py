import unittest
import os
import sys
import json
from rdflib import RDF,Graph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
from networkx.readwrite import json_graph

sys.path.insert(0, os.path.join(".."))
from converters.instance_converter import convert as instance_convert
from converters.model_converter import convert as model_convert
from converters.sbol.utility.graph import SBOLGraph

from graph.instance_graph import InstanceGraph
from utility.nv_identifiers import identifiers as nv_ids

curr_dir = os.path.dirname(os.path.realpath(__file__))
model_fn = os.path.join(curr_dir,"..","utility","nv_model.xml")



class TestConvertModel(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        None

    def _graph_element_check(self,graph):
        '''
        Checks no keys are mapping correctly.
        '''
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

    def test_convert(self):
        rdf_g = Graph()
        rdf_g.load(model_fn)

        nx_graph = model_convert(rdf_g)
        for s,p,o in rdf_g.triples((None,None,None)):
            self.assertTrue(is_node(nx_graph,s))
            self.assertTrue(is_node(nx_graph,o))
            self.assertTrue(is_edge(nx_graph,s,p,o))
        rdf_conv_g = rdflib_to_networkx_multidigraph(rdf_g)
        self.assertTrue(nx_graph == rdf_conv_g)
        self._graph_element_check(nx_graph)

class TestConvertInstance(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        None

    def test_convert_combined(self):
        filename = os.path.join(curr_dir,"files","multiplexer.xml")
        json_file = os.path.join(curr_dir,"files","multiplexer.json")
        sbol_graph = instance_convert(filename)
        sbol_graph.save(json_file)
        nv_graph = instance_convert(json_file)
        self.assertTrue(nv_graph == sbol_graph)

    def test_convert_nv(self):
        filename = os.path.join(curr_dir,"files","multiplexer.xml")
        json_file = os.path.join(curr_dir,"files","multiplexer.json")
        graph = instance_convert(filename)
        
        graph.save(json_file)
        graph = instance_convert(json_file)
        with open(json_file) as f:
            data = json.load(f)
        expected_g = InstanceGraph(json_graph.node_link_graph(data))
        self.assertTrue(graph == expected_g)

    def test_convert_sbol(self):
        filename = os.path.join(curr_dir,"files","multiplexer.xml")
        graph = instance_convert(filename)
        rdf_graph = SBOLGraph(filename)
        rdf_cds =  rdf_graph.get_component_definitions()
        for cd in rdf_cds:
            self.assertTrue(is_node(graph,cd))
            self.assertTrue(is_edge(graph,cd,RDF.type,nv_ids.objects.entity))
            for c in rdf_graph.get_components(cd):
                definition = rdf_graph.get_definition(c)
                self.assertTrue(is_node(graph,definition))
                self.assertTrue(is_edge(graph,cd,nv_ids.predicates.contains,definition))


def is_node(graph,subject):
    for n,data in graph.nodes(data=True):
        if subject == data["key"]:
            return True
    return False

def is_edge(graph,s,p,o):
    for n,v,k in graph.edges(keys=True):
        n_k = graph.nodes[n]["key"]
        v_k = graph.nodes[v]["key"]
        if s == n_k and p == k and o == v_k:
            return True
    return False

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
