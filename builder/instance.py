from converters.instance import convert
from builder.abstract import AbstractBuilder
from builder.builders.instance.view import ViewBuilder
from builder.builders.instance.mode import ModeBuilder

class InstanceBuilder(AbstractBuilder):
    def __init__(self,graph):
        super().__init__(convert(graph))
        self._view_h = ViewBuilder(self)
        self._mode_h = ModeBuilder(self)

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
