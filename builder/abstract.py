import networkx as nx
from rdflib import RDF
import re

class AbstractBuilder:
    def __init__(self,graph):
        self._graph = graph
        self.view = self._graph
        
    @property
    def nodes(self):
        return self._graph.nodes

    @property
    def edges(self):
        return self._graph.edges
    
    @property
    def v_nodes(self):
        return self.view.nodes
    
    @property
    def v_edges(self):
        return self.view.edges

    @property
    def graph(self):
        return self.view
    
    def get_node_data(self,node_id):
        node_id = self._resolve_subject(node_id)
        try:
            return self.nodes[node_id]
        except KeyError:
            pass
        try:
            return self.v_nodes[node_id]
        except KeyError:
            return None

    def get_next_index(self):
        return max([i for i in self._graph.nodes])

    def in_edges(self,node = None,keys = False):
        return self.view.in_edges(node,keys=keys)
    
    def out_edges(self,node = None,keys = False):
        return self.view.out_edges(node,keys = keys)
        
    def set_network_mode(self):
        self.view = self._mode_h.network()
    
    def set_tree_mode(self):
        self.view = self._mode_h.tree()

    def set_full_view(self):
        self.view = self._view_h.full()

    def sub_graph(self,edges,node_attrs = {}):
        new_graph = nx.MultiDiGraph()
        new_graph.add_edges_from(edges)
        for k,v in node_attrs.items():
            new_graph.add_node(k,**v)
        new_graph = self._graph.__class__(new_graph)
        return new_graph

    def get_rdf_type(self,subject):
        subject = self._resolve_subject(subject)
        return self._graph.get_rdf_type(subject)

    def get_namespace(self,uri):
        split_subject = _split(uri)
        if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
            name = split_subject[-2]
        else:
            name = split_subject[-1]
        return uri.split(name)[0]
    
    def resolve_list(self,list_id):
        elements = []
        list_id = self._resolve_subject(list_id)
        next_id = list_id
        while True:
            res = self._graph.search((next_id,None,None))
            f = [c[1] for c in res if c[2] == RDF.first]
            r = [c[1] for c in res if c[2] == RDF.rest]
            if len(f) != 1 or len(r) != 1:
                raise ValueError(f'{list_id} is a malformed list.')
            elements.append(f[0])
            r,r_data = r[0]
            if r_data["key"] == RDF.nil:
                break
            next_id = r
        return elements

    def _resolve_subject(self,subject):
        if subject in self._graph:
            return subject
        if subject in self.view:
            key = self.view.nodes[subject]["key"]
            for n,data in self._graph.nodes(data=True):
                if data["key"] == key:
                    return n
            else:
                return subject
        raise ValueError(f'{subject} Not in either graph or viewgraph.')

def _split(uri):
    return re.split('#|\/|:', uri)