from rdflib import OWL,RDF

from converters.model_handler import convert
from builder.abstract import AbstractBuilder
from builder.builders.model.view import ViewBuilder
from builder.builders.model.mode import ModeBuilder

class ModelBuilder(AbstractBuilder):
    def __init__(self,graph):
        super().__init__(convert(graph))
        self._view_h = ViewBuilder(self)
        self._mode_h = ModeBuilder(self)
        self.identifiers = self._graph.identifiers


    def set_hierarchy_view(self):
        self.view = self._view_h.hierarchy()
    
    def set_requirements_view(self):
        self.view = self._view_h.requirements()

    def set_relation_view(self):
        self.view = self._view_h.relation()

    # -------------------- Queries --------------------
    def get_classes(self,bnodes=True):
        return self._graph.get_classes(bnodes)

    def get_parent_classes(self,class_id):
        class_id = self._resolve_subject(class_id)
        return self._graph.get_parent_classes(class_id)

    def get_child_classes(self,class_id):
        class_id = self._resolve_subject(class_id)
        return self._graph.get_child_classes(class_id)

    def get_class_depth(self,class_id):
        class_id = self._resolve_subject(class_id)
        return self._graph.get_class_depth(class_id)
   
    def get_base_class(self):
        return self._graph.get_base_class()

    def get_equivalent_classes(self,class_id):
        class_id = self._resolve_subject(class_id)
        return self._graph.get_equivalent_classes(class_id)

    def get_properties(self):
        return self._graph.get_properties()
    
    def get_range(self,subject):
        subject = self._resolve_subject(subject)
        return self._graph.get_range(subject)

    def get_domain(self,subject):
        subject = self._resolve_subject(subject)
        return self._graph.get_domain(subject)

    def get_union(self,subject):
        subject = self._resolve_subject(subject)
        return self._graph.get_union(subject)
    
    def resolve_union(self,subject):
        return self._graph.resolve_union(subject)
        
    def get_class_properties(self,class_id):
        class_id = self._resolve_subject(class_id)
        return self._graph.get_properties(class_id)