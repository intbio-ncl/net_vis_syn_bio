from rdflib import RDF

from converters import converter
from builder.builders.view import ViewBuilder
from builder.builders.mode import ModeBuilder

class NVBuilder:
    def __init__(self,graph):
        self._graph = converter.convert(graph)
        self.view = self._graph
        self._view_h = ViewBuilder(self._graph)
        self._mode_h = ModeBuilder(self._graph)

    @property
    def nodes(self):
        return self.view.nodes

    @property
    def edges(self):
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

    def set_components_view(self):
        self.view = self._view_h.components()

    def set_interaction_verbose_view(self):
        self.view = self._view_h.verbose()

    def set_interaction_view(self):
        self.view = self._view_h.interaction()

    def set_genetic_interaction_view(self):
        self.view = self._view_h.genetic_interaction()

    def set_ppi_view(self):
        self.view = self._view_h.ppi()

    def set_module_view(self):
        self.view = self._view_h.module_view()
                                              
    def set_maps_view(self):
        self.view = self._view_h.maps()

    def get_entity_code(self,entity):
        for node,data in self.nodes(data=True):
            if data["key"] == entity or node == entity:
                return node
        raise ValueError(f"Can't find code for {entity}")


    def get_rdf_type(self,subject):
        subject = self._resolve_subject(subject)
        rdf_type = self._graph.search((subject,RDF.type,None),lazy=True)
        if rdf_type != []:
            return rdf_type[1]

    def _resolve_subject(self,subject):
        if subject in self._graph:
            return subject
        if subject in self.view:
            key = self.view.nodes[subject]["key"]
            for n,data in self._graph.nodes(data=True):
                if data["key"] == key:
                    return n
        raise ValueError(f'{subject} Not in either graph or viewgraph.')
