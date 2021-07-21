import networkx as nx
from rdflib import Graph,RDF

from converters.sbol import convert as sbol_convert
from converters.nv import convert as nv_convert
from graph.graph import NVGraph

convert_dict = {"sbol" : sbol_convert,
                "nv"   : nv_convert}

def convert(filename,convert_type=None):
    if convert_type is None:
        convert_type = derive_convert_type(filename)
    graph = convert_dict[convert_type].convert(filename)
    return NVGraph(graph)

def get_converter_names():
    return list(convert_dict.keys())
    
def derive_convert_type(filename):
    if filename.endswith(".xml"):
        return "sbol"
    elif filename.endswith(".json"):
        return "nv"