from rdflib import RDF

from converters.instance import convert as i_convert
from converters.model import convert as m_convert

from builder.abstract import AbstractBuilder
from builder.builders.instance.view import ViewBuilder
from builder.builders.instance.mode import ModeBuilder

class InstanceBuilder(AbstractBuilder):
    def __init__(self,model,graph=None):
        model_graph = m_convert(model)
        super().__init__(i_convert(model_graph,graph))
        self._model_graph = model_graph
        self._view_h = ViewBuilder(self)
        self._mode_h = ModeBuilder(self)

    def load(self,fn):
        self._graph = i_convert(self._model_graph,fn)

    def set_pruned_view(self):
        self.view = self._view_h.pruned()
         
    def set_hierarchy_view(self):
        self.view = self._view_h.hierarchy()

    def set_interaction_verbose_view(self):
        self.view = self._view_h.interaction_verbose()

    def set_interaction_view(self):
        self.view = self._view_h.interaction()

    def set_interaction_genetic_view(self):
        self.view = self._view_h.genetic_interaction()

    def set_protein_protein_interaction_view(self):
        self.view = self._view_h.protein_interaction()

    def set_ppi_view(self):
        self.view = self._view_h.ppi()

    def set_module_view(self):
        self.view = self._view_h.module_view()

    def get_entities(self):
        classes = [c[1]["key"] for c in self._model_graph.get_classes(False)]
        return [c[0] for c in self._graph.search((None,RDF.type,classes))]

    def get_children(self,subject):
        subject = self._resolve_subject(subject)
        cp = self._model_graph.get_child_predicate()
        return [c[1:3] for c in self._graph.search((subject,cp,None))]
    
    def get_parents(self,subject):
        subject = self._resolve_subject(subject)
        cp = self._model_graph.get_child_predicate()
        return [c[0:3:2] for c in self._graph.search((None,cp,subject))]

    def get_entity_depth(self,subject):
        def _get_class_depth(s,depth):
            parent = self.get_parents(s)
            if parent == []:
                return depth
            depth += 1
            c_identifier = parent[0][0][0]
            return _get_class_depth(c_identifier,depth)
        return _get_class_depth(subject,0)

    def get_root_entities(self):
        roots = []
        for entity in self.get_entities():
            if self.get_parents(entity[0]) == []:
                roots.append(entity)
        return roots