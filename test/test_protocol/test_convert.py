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

from converters.protocol_handler import convert as protocol_convert
from converters.model_handler import convert as model_convert

curr_dir = os.path.dirname(os.path.realpath(__file__))
model_fn = os.path.join(curr_dir,"..","..","utility","nv_protocol.xml")
test_dir = os.path.join(curr_dir,"..","files")

class TestConvertDesign(unittest.TestCase):

    def setUp(self):
        None

    def tearDown(self):
        None

    def test_sbol_cds(self):
        filename = os.path.join(test_dir,"ot2.py")
        model_graph = model_convert(model_fn)
        graph = protocol_convert(model_graph,filename)

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
