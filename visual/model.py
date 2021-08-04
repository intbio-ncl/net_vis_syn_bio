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
    def set_heirarchy_preset(self):
        '''
        Pre-set methods with an affinity for displaying the pruned graph view.
        '''
        preset_functions = [self.set_tree_mode,
                            self.set_heirarchy_view,
                            self.set_dagre_layout,
                            self.add_node_name_labels,
                            self.add_edge_no_labels,
                            self.add_branch_node_color,
                            self.add_standard_edge_color,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_straight_edge_shape]
        return self._set_preset(preset_functions)

    # ---------------------- View -----------------------------
    def set_heirarchy_view(self):
        '''
        View of the heirachy of Classes taken from the ontology.
        '''
        if self.view == self.set_heirarchy_view:
            self._builder.set_heirarchy_view()
        else:
           self.view =self.set_heirarchy_view
    
    def set_requirements_view(self):
        '''
        Sub graph viewing the heirachy combined with 
        the requirements to build a given Class.
        '''
        if self.view == self.set_requirements_view:
            self._builder.set_requirements_view()
        else:
           self.view =self.set_requirements_view

    # ---------------------- Node Labels ----------------------


    # ---------------------- Edge Labels ----------------------


    # ---------------------- Node Color -----------------------
    def add_branch_node_color(self):
        '''
        Each branch from the root node is a different color (Increased tint).
        '''
        if self.node_color == self.add_role_node_color:
            return self._color_h.node.branch(self._builder)
        else:
            self.node_color = self.add_role_node_color

    
    def add_heirarchy_node_color(self):
        '''
        Further from the root, shade is decreased.
        '''
        if self.node_color == self.add_heirarchy_node_color:
            return self._color_h.node.heirarchy(self._builder)
        else:
            self.node_color = self.add_heirarchy_node_color



    # ---------------------- Edge Color ----------------------
    def add_type_edge_color(self):
        '''
        All proprietary edge types are colored.
        ''' 
        if self.edge_color == self.add_type_edge_color:
            return self._color_h.edge.predicate(self._builder)
        else:
            self.edge_color = self.add_type_edge_color


    # ---------------------- Node Size ----------------------
    def add_heirachy_node_size(self):
        '''
        Each level from the root node is smaller than parent.
        '''
        if self.node_size == self.add_hierarchy_node_size:
            return self._size_h.hierarchy(self._builder)
        else:
            self.node_size = self.add_hierarchy_node_size
