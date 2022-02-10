import networkx as nx
import json
from rdflib import URIRef
from rdflib import Literal
from rdflib import BNode

accepted_file_types = ['protocol.nv']
def convert(filename,model_graph):
    graph = nx.MultiDiGraph()

    with open(filename) as f:
        data = json.load(f)

    for node in data["nodes"]:
        id = node["id"]
        n_type = node["type"]
        if n_type == "URI":
            node["key"] = URIRef(node["key"])
        elif n_type == "BNode":
            node["key"] = BNode(node["key"])
        else:
            node["key"] = Literal(node["key"])
        del node["id"]
        graph.add_node(id,**node)

    for edge in data["links"]:
        source = edge["source"]
        target = edge["target"]
        key = URIRef(edge["key"])
        del edge["source"]
        del edge["target"]
        del edge["key"]
        graph.add_edge(source,target,key,**edge)
    return graph
