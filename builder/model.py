from rdflib import RDFS,OWL,RDF,BNode
import networkx as nx

from utility.identifiers import produce_identifiers
from converters.model import convert
from builder.abstract import AbstractBuilder
from builder.builders.model.view import ViewBuilder
from builder.builders.model.mode import ModeBuilder

class ModelBuilder(AbstractBuilder):
    def __init__(self,graph):
        super().__init__(convert(graph))
        self._view_h = ViewBuilder(self)
        self._mode_h = ModeBuilder(self)
        self._identifiers = produce_identifiers(self._graph)


    def set_heirarchy_view(self):
        self.view = self._view_h.heirarchy()

    def get_classes(self):
        return [c[0] for c in self._graph.search((None,RDF.type,OWL.Class))]

    def get_parent_classes(self,class_id):
        class_id = self._resolve_subject(class_id)
        return [c[1] for c in self._graph.search((class_id,RDFS.subClassOf,None))]

    def get_base_class(self):
        bases = []
        for c,data in self.get_classes():
            if isinstance(data["key"], BNode):
                continue
            parents = self.get_parent_classes(c)
            if len(parents) == 0:
                bases.append([c,data])
        return bases

    def get_child_classes(self,class_name):
        return [c[0] for c in self._graph.search((None,RDFS.subClassOf,class_name))]
    
    def get_requirements(self,class_name):
        pass
    
