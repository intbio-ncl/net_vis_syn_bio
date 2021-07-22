import unittest
import os
import sys
import json
from rdflib import Graph,RDF
import networkx as nx
from networkx.readwrite import json_graph

sys.path.insert(0, os.path.join("..","..","..",".."))
sys.path.insert(0, os.path.join("..","..",".."))
sys.path.insert(0, os.path.join("..",".."))

from converters.converter import convert
from graph.graph import NVGraph
from converters.sbol.identifiers import identifiers
from utility.nv_identifiers import identifiers as nv_ids

curr_dir = os.path.dirname(os.path.realpath(__file__))

class TestConvert(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        None



    def test_convert_combined(self):
        graphs = []
        t_dir = os.path.join(curr_dir,"files")
        for file in os.listdir(t_dir):
            fn = os.path.join(t_dir,file)
            graphs.append(convert(fn))
        
        for index,g in enumerate(graphs):
            if index == len(graphs) -1:
                continue
            self.assertTrue(g == graphs[index + 1])

    def test_convert_nv(self):
        filename = os.path.join(curr_dir,"files","test_convert.json")
        graph = convert(filename)
        with open(filename) as f:
            data = json.load(f)
        expected_g = NVGraph(json_graph.node_link_graph(data))
        self.assertTrue(graph == expected_g)

    def test_convert_sbol(self):
        '''
        Might need another look over when the underlying dm is worked on ...
        '''

        filename = os.path.join(curr_dir,"files","test_convert.xml")
        graph = convert(filename,"sbol")
        rdf_graph = Graph()
        rdf_graph.load(filename)
        
        rdf_cds =  rdf_graph.triples((None,RDF.type,identifiers.objects.component_definition))
        rdf_ints = rdf_graph.triples((None,RDF.type,identifiers.objects.interaction))


        for s,p,o in rdf_cds:
            self.assertTrue(is_node(graph,s))
            self.assertTrue(is_edge(graph,s,p,nv_ids.objects.entity))

        for s,p,o in rdf_ints:
            self.assertTrue(is_node(graph,s))
            self.assertTrue(is_edge(graph,s,p,nv_ids.objects.interaction))


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
