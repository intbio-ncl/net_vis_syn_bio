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
        self.view = self._view_h.verbose()

    def set_interaction_view(self):
        self.view = self._view_h.interaction()

    def set_interaction_genetic_view(self):
        self.view = self._view_h.genetic_interaction()

    def set_ppi_view(self):
        self.view = self._view_h.ppi()

    def set_module_view(self):
        self.view = self._view_h.module_view()
