import os
import dash_cytoscape as cyto
cyto.load_extra_layouts()
from builder.model import ModelBuilder
from visual.abstract import AbstractVisual

from visual.handlers.model.layout import LayoutHandler
from visual.handlers.model.label import LabelHandler
from visual.handlers.model.color import ColorHandler
from visual.handlers.model.size import SizeHandler
from visual.handlers.model.shape import ShapeHandler

default_stylesheet_fn = os.path.join(os.path.dirname(os.path.realpath(__file__)),"default_stylesheet.txt")
class ModelVisual(AbstractVisual):
    def __init__(self,graph=None):
        super().__init__()
        if graph is None:
            self._builder = None
        elif isinstance(graph,ModelBuilder):
            self._builder = graph
        else:
            self._builder = ModelBuilder(graph)

        self._layout_h = LayoutHandler()
        self._label_h = LabelHandler()
        self._color_h = ColorHandler()
        self._size_h = SizeHandler()
        self._shape_h = ShapeHandler()


    # ---------------------- Preset ----------------------------


    # ---------------------- View -----------------------------
    def set_heirarchy_view(self):
        '''
        Sub graph viewing the raw graph with specific edges removed 
        that are deemed not useful for visualisation.
        '''
        if self.view == self.set_heirarchy_view:
            self._builder.set_heirarchy_view()
        else:
           self.view =self.set_heirarchy_view
    
    # ---------------------- Node Labels ----------------------


    # ---------------------- Edge Labels ----------------------


    # ---------------------- Node Color ----------------------- 


    # ---------------------- Edge Color ----------------------


    # ---------------------- Node Size ----------------------
