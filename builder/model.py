from rdflib import RDFS,OWL
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

    def get_sub_classes(self,class_name):
        return self._graph.search((class_name,RDFS.subClassOf,None))

    def get_requirements(self,class_name):
        pass
    


    def _build_model_identifiers()