from converters.model import convert
from builder.abstract import AbstractBuilder
from builder.builders.model.view import ViewBuilder
from builder.builders.model.mode import ModeBuilder

class ModelBuilder(AbstractBuilder):
    def __init__(self,graph):
        super().__init__(convert(graph))
        self._view_h = ViewBuilder(self)
        self._mode_h = ModeBuilder(self)


    def set_hierarchy_view(self):
        self.view = self._view_h.hierarchy()
    
    def set_requirements_view(self):
        self.view = self._view_h.requirements()

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