import networkx as nx
from rdflib import RDF

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
        for subject,node,edge in new_graph.edges:
            try:
                new_graph.nodes[subject].update(node_attrs[subject])
            except (KeyError,ValueError):
                pass
            try:
                new_graph.nodes[node].update(node_attrs[node])
            except (KeyError,ValueError):
                pass
        new_graph = self._graph.__class__(new_graph)
        return new_graph

    def get_rdf_type(self,subject):
        subject = self._resolve_subject(subject)
        return self._graph.get_rdf_type(subject)

    def _resolve_subject(self,subject):
        if subject in self._graph:
            return subject
        if subject in self.view:
            key = self.view.nodes[subject]["key"]
            for n,data in self._graph.nodes(data=True):
                if data["key"] == key:
                    return n
        raise ValueError(f'{subject} Not in either graph or viewgraph.')