from converters.protocol_handler import convert as p_convert
from converters.model_handler import convert as m_convert

from builder.abstract import AbstractBuilder
from builder.builders.protocol.view import ViewBuilder
from builder.builders.protocol.mode import ModeBuilder

class ProtocolBuilder(AbstractBuilder):
    def __init__(self,model,graph=None):
        model_graph = m_convert(model)
        super().__init__(p_convert(model_graph,graph))
        self._model_graph = model_graph
        self._view_h = ViewBuilder(self)
        self._mode_h = ModeBuilder(self)

    def load(self,fn):
        self._graph = p_convert(self._model_graph,fn)