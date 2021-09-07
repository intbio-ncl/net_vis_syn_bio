import unittest
import os
import sys
import re
import json

from rdflib import RDF
from networkx.readwrite import json_graph
from rdflib.term import URIRef

sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))
sys.path.insert(0, os.path.join("..","..",".."))

from converters.instance import convert as instance_convert
from converters.model import convert as model_convert
from converters.sbol.utility.graph import SBOLGraph
from graph.instance import InstanceGraph

curr_dir = os.path.dirname(os.path.realpath(__file__))
model_fn = os.path.join(curr_dir,"..","..","utility","nv_model.xml")
test_dir = os.path.join(curr_dir,"..","files")

class TestConvertInstance(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        None

    def test_sbol_cds(self):
        filename = os.path.join(test_dir,"test_convert_sbol_cds.xml")
        model_graph = model_convert(model_fn)
        graph = instance_convert(model_graph,filename)
        rdf_graph = SBOLGraph(filename)
        subjects = [t[0] for t in rdf_graph.search((None,None,None))]

        for n,v,k in graph.edges(keys=True):
            n_data = graph.nodes[n]
            v_data = graph.nodes[v]
            self.assertIn(n_data["key"],subjects)
            if k == RDF.type:
                # Purposefully named entities same as types for testing.
                e_t = _get_name(n_data["key"])
                a_t = _get_name(v_data["key"])
                self.assertEqual(a_t,e_t)

    def test_sbol_entity_entity(self):
        filename = os.path.join(test_dir,"test_convert_sbol_entity_entity.xml")
        model_graph = model_convert(model_fn)
        graph = instance_convert(model_graph,filename)
        rdf_graph = SBOLGraph(filename)
        expected_edges = []

        for cd in rdf_graph.get_component_definitions():
            related_cds = [rdf_graph.get_definition(c) for c in rdf_graph.get_components(cd)]
            [expected_edges.append((cd,None,rc)) for rc in related_cds]
        
        part_of_pred = URIRef("http://www.nv_ontology.org/partOf")
        edge_keys = [k for n,v,k in graph.edges(keys=True)]
        e_e_edges = [k for k in edge_keys if k == part_of_pred]
        self.assertEqual(len(e_e_edges),len(expected_edges))
        for n,v,k in graph.edges(keys=True):
            print(n,v,k)
            if k != part_of_pred:
                continue
            n_data = graph.nodes[n]
            v_data = graph.nodes[v]
            actual_edge = (n_data["key"],None,v_data["key"])
            self.assertIn(actual_edge,expected_edges)
        
    def test_sbol_interactions(self):
        filename = os.path.join(test_dir,"test_sbol_interactions.xml")
        model_graph = model_convert(model_fn)
        graph = instance_convert(model_graph,filename)
        rdf_graph = SBOLGraph(filename)
        expected_edges = []

    def test_convert_sbol(self):
        filename = os.path.join(test_dir,"multiplexer.xml")
        model_graph = model_convert(model_fn)
        graph = instance_convert(model_graph,filename)
        rdf_graph = SBOLGraph(filename)
        expected_edges = []

        for cd in rdf_graph.get_component_definitions():
            related_cds = [rdf_graph.get_definition(c) for c in rdf_graph.get_components(cd)]
            [expected_edges.append((cd,None,rc)) for rc in related_cds]
        
        part_of_pred = URIRef("http://www.nv_ontology.org/partOf")
        edge_keys = [k for n,v,k in graph.edges(keys=True)]
        e_e_edges = [k for k in edge_keys if k == part_of_pred]
        self.assertEqual(len(e_e_edges),len(expected_edges))
        for n,v,k in graph.edges(keys=True):
            if k != part_of_pred:
                continue
            n_data = graph.nodes[n]
            v_data = graph.nodes[v]
            actual_edge = (n_data["key"],None,v_data["key"])
            self.assertIn(actual_edge,expected_edges)

    def test_convert_nv(self):
        model_graph = model_convert(model_fn)
        filename = os.path.join(test_dir,"multiplexer.xml")
        json_file = os.path.join(test_dir,"multiplexer.json")
        graph = instance_convert(model_graph,filename)
        
        graph.save(json_file)
        graph = instance_convert(model_graph,json_file)
        with open(json_file) as f:
            data = json.load(f)
        expected_g = InstanceGraph(json_graph.node_link_graph(data))
        self.assertTrue(graph == expected_g)

    def test_convert_combined(self):
        model_graph = model_convert(model_fn)
        filename = os.path.join(test_dir,"multiplexer.xml")
        json_file = os.path.join(test_dir,"multiplexer.json")
        sbol_graph = instance_convert(model_graph,filename)
        sbol_graph.save(json_file)
        nv_graph = instance_convert(model_graph,json_file)
        self.assertTrue(nv_graph == sbol_graph)


def _get_name(subject):
    split_subject = _split(subject)
    if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
        return split_subject[-2]
    else:
        return split_subject[-1]

def _split(uri):
    return re.split('#|\/|:', uri)

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
