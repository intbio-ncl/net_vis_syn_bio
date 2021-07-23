import unittest
import os
import sys
import json
from rdflib import RDF
import networkx as nx
from networkx.readwrite import json_graph

sys.path.insert(0, os.path.join(".."))

from converters.converter import convert
from graph.graph import NVGraph
from converters.sbol.utility.graph import SBOLGraph
from utility.nv_identifiers import identifiers as nv_ids

curr_dir = os.path.dirname(os.path.realpath(__file__))

class TestConvert(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        None

    def test_convert_combined(self):
        filename = os.path.join(curr_dir,"files","multiplexer.xml")
        json_file = os.path.join(curr_dir,"files","multiplexer.json")
        sbol_graph = convert(filename)
        sbol_graph.save(json_file)
        nv_graph = convert(json_file)
        self.assertTrue(nv_graph == sbol_graph)

    def test_convert_nv(self):
        filename = os.path.join(curr_dir,"files","multiplexer.xml")
        json_file = os.path.join(curr_dir,"files","multiplexer.json")
        graph = convert(filename)
        
        graph.save(json_file)
        graph = convert(json_file)
        with open(json_file) as f:
            data = json.load(f)
        expected_g = NVGraph(json_graph.node_link_graph(data))
        self.assertTrue(graph == expected_g)

    def test_convert_sbol(self):
        '''
        Might need another look over when the underlying dm is worked on ...
        '''
        filename = os.path.join(curr_dir,"files","multiplexer.xml")
        graph = convert(filename,"sbol")
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
