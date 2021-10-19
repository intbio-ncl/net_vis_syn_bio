import os

import dash_cytoscape as cyto
cyto.load_extra_layouts()
from builder.protocol import ProtocolBuilder
from visual.abstract import AbstractVisual
from visual.handlers.protocol.layout import LayoutHandler
from visual.handlers.protocol.label import LabelHandler
from visual.handlers.protocol.color import ColorHandler
from visual.handlers.protocol.size import SizeHandler
from visual.handlers.protocol.shape import ShapeHandler

default_stylesheet_fn = os.path.join(os.path.dirname(os.path.realpath(__file__)),"default_stylesheet.txt")

class ProtocolVisual(AbstractVisual):
    def __init__(self,model,graph=None):
        super().__init__()
        self._builder = ProtocolBuilder(model,graph)
        self._layout_h = LayoutHandler()
        self._label_h = LabelHandler(self._builder)
        self._color_h = ColorHandler(self._builder)
        self._size_h = SizeHandler(self._builder)
        self._shape_h = ShapeHandler(self._builder)
        self.set_concentric_layout()

    def _load_graph(self,fn):
        return self._builder.load(fn)

    # ---------------------- Preset --------------------------------------
    # ---------------------- View ----------------------------------------     
    # ---------------------- Node Labels --------------------------------- 
    # ---------------------- Edge Labels ---------------------------------
    # ---------------------- Node Color ----------------------------------
    # ---------------------- Edge Color ----------------------------------
    # ---------------------- Node Size -----------------------------------