from rdflib import RDF
import networkx as nx

from converters import converter
from builder.builders.view import ViewBuilder
from builder.builders.mode import ModeBuilder
from utility.nv_identifiers import identifiers
from graph.graph import NVGraph

class NVBuilder:
    def __init__(self,graph):
        self._graph = converter.convert(graph)
        self.view = self._graph
        self._view_h = ViewBuilder(self)
        self._mode_h = ModeBuilder(self)

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

    def set_pruned_view(self):
        self.view = self._view_h.pruned()
         
    def set_heirarchy_view(self):
        self.view = self._view_h.heirarchy()

    def set_interaction_verbose_view(self):
        self.view = self._view_h.verbose()

    def set_interaction_view(self):
        self.view = self._view_h.interaction()

    def set_interaction_genetic_view(self):
        self.view = self._view_h.genetic_interaction()

    def set_ppi_view(self):
        self.view = self._view_h.ppi()

    def set_module_view(self):
        self.view = self._view_h.module_view()

    def get_rdf_type(self,subject):
        subject = self._resolve_subject(subject)
        rdf_type = self._graph.search((subject,RDF.type,None),lazy=True)
        if rdf_type != []:
            return rdf_type[1]

    def get_entities(self,entity=None):
        if entity is not None:
            entity = self._resolve_subject(entity)
            return [e[1] for e in self._graph.search((entity,identifiers.predicates.contains,None))]
        return [e[0] for e in self._graph.search((None,RDF.type,identifiers.objects.entity))]

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
        new_graph = NVGraph(new_graph)
        return new_graph

    def _resolve_subject(self,subject):
        if subject in self._graph:
            return subject
        if subject in self.view:
            key = self.view.nodes[subject]["key"]
            for n,data in self._graph.nodes(data=True):
                if data["key"] == key:
                    return n
        raise ValueError(f'{subject} Not in either graph or viewgraph.')
