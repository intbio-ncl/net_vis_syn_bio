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
        def none(self,view):
            return [None] * len(view.nodes())
        
        def adjacency(self,view):
            node_text = []
            for node in view.nodes:
                num_in = len(view.in_edges(node))
                num_out = len(view.out_edges(node)) 
                node_text.append(f"# IN: {str(num_in)}, # OUT: {str(num_out)}")
            return node_text

        def name(self,view):
            node_text = []
            names = nx.get_node_attributes(view,"display_name")
            for v in names.values():
                node_text.append(v)
            return node_text

        def type(self,view,graph):
            node_text = []
            for node in view.nodes:
                for n,v,e in graph.edges(node,keys=True):
                    if e[1] == RDF.type:
                        node_text.append(_get_name(str(e[2])))
                        break
                else:
                    if isinstance(e[2],Literal):
                        node_text.append("Literal")
                    elif isinstance(e[2],URIRef):
                        node_text.append("Identifier")
                    else:
                        node_text.append("?")
            return node_text

        def role(self,view,graph):
            print("WARN:: Not Implemented")
            node_text = []
            for node in view.nodes:
                node_text.append(None)
            return node_text

    class EdgeLabelHandler:
        def __init__(self):
            pass
        def none(self,view):
            return [None] * len(view.edges())

        def name(self,view):
            edge_names = []
            for edge in view.edges(data=True):
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