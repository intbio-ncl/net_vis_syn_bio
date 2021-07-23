import re
import networkx as nx
from rdflib import URIRef,Literal,RDF

class LabelHandler:
    def __init__(self):
        self.node = self.NodeLabelHandler()
        self.edge = self.EdgeLabelHandler()
    

    class NodeLabelHandler:
        def __init__(self):
            pass
        def none(self,builder):
            return [None] * len(builder.v_nodes())
        
        def adjacency(self,builder):
            node_text = []
            for node in builder.v_nodes:
                num_in = len(builder.in_edges(node))
                num_out = len(builder.out_edges(node)) 
                node_text.append(f"# IN: {str(num_in)}, # OUT: {str(num_out)}")
            return node_text

        def name(self,builder):
            names = []
            for node,data in builder.v_nodes(data=True):
                names.append(data["display_name"])
            return names

        def type(self,builder):
            node_text = []
            for node,data in builder.v_nodes(data=True):
                key = data["key"]
                if builder.get_rdf_type(node) is not None:
                    node_text.append(_get_name(key))
                else:
                    if isinstance(key,Literal):
                        node_text.append("Literal")
                    elif isinstance(key,URIRef):
                        node_text.append("Identifier")
                    else:
                        node_text.append("?")
            return node_text

        def role(self,builder):
            print("WARN:: Not Implemented")
            node_text = []
            for node in builder.v_nodes:
                node_text.append(None)
            return node_text

    class EdgeLabelHandler:
        def __init__(self):
            pass
        def none(self,builder):
            return [None] * len(builder.v_edges())

        def name(self,builder):
            edge_names = []
            for edge in builder.v_edges(data=True):
                edge_names.append(edge[2]["display_name"])
            return edge_names


def _get_name(subject):
    split_subject = _split(subject)
    if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
        return split_subject[-2]
    elif len(split_subject[-1]) == 3 and _isfloat(split_subject[-1]):
        return split_subject[-2]
    else:
        return split_subject[-1]

def _split(uri):
    return re.split('#|\/|:', uri)

def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False