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
            self._builder = ModelBuilder(graph)
        elif isinstance(graph,ModelBuilder):
            self._builder = graph
        else:
            self._builder = ModelBuilder(graph)
        
        self._layout_h = LayoutHandler()
        self._label_h = LabelHandler(self._builder)
        self._color_h = ColorHandler(self._builder)
        self._size_h = SizeHandler(self._builder)
        self._shape_h = ShapeHandler(self._builder)
        self.set_concentric_layout()


    # ---------------------- Preset ----------------------------
    def set_hierarchy_preset(self):
        '''
        Methods for displaying the inheritence tree encoded within the model.
        '''
        preset_functions = [self.set_tree_mode,
                            self.set_hierarchy_view,
                            self.set_dagre_layout,
                            self.add_node_name_labels,
                            self.add_edge_no_labels,
                            self.add_hierarchy_node_color,
                            self.add_hierarchy_edge_color,
                            self.add_hierarchy_node_size,
                            self.set_circle_node_shape,
                            self.set_straight_edge_shape]
        return self._set_preset(preset_functions)

    def set_requirements_preset(self):
        '''
        Methods for displaying what is required to realise a given class within the model.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_requirements_view,
                            self.set_cola_layout,
                            self.add_node_name_labels,
                            self.add_edge_no_labels,
                            self.add_branch_node_color,
                            self.add_branch_edge_color,
                            self.add_standard_node_size,
                            self.add_logic_node_shape,
                            self.set_straight_edge_shape]
        return self._set_preset(preset_functions)

    def set_relation_preset(self):
        '''
        Method for displaying relationships between classes within the model.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_relation_view,
                            self.set_cola_layout,
                            self.add_node_name_labels,
                            self.add_edge_name_labels,
                            self.add_class_node_color,
                            self.add_type_edge_color,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_straight_edge_shape]
        return self._set_preset(preset_functions)

    # ---------------------- View -----------------------------
    def set_hierarchy_view(self):
        '''
        View of the heirachy of Classes taken from the ontology.
        '''
        if self.view == self.set_hierarchy_view:
            self._builder.set_hierarchy_view()
        else:
           self.view =self.set_hierarchy_view
    
    def set_requirements_view(self):
        '''
        Sub graph viewing the heirachy combined with 
        the requirements to build a given Class.
        '''
        if self.view == self.set_requirements_view:
            self._builder.set_requirements_view()
        else:
           self.view =self.set_requirements_view

    def set_relation_view(self):
        '''
        View the relationship between entities within Model.
        '''
        if self.view == self.set_relation_view:
            self._builder.set_relation_view()
        else:
           self.view =self.set_relation_view

    # ---------------------- Node Labels ----------------------


    # ---------------------- Edge Labels ----------------------


    # ---------------------- Node Color -----------------------
    def add_class_node_color(self):
        '''
        Each Class is mapped to a distinct color.
        '''
        if self.node_color == self.add_class_node_color:
            return self._color_h.node.nv_class()
        else:
            self.node_color = self.add_class_node_color

    def add_branch_node_color(self):
        '''
        Each branch from the root node is a different color.
        '''
        if self.node_color == self.add_branch_node_color:
            return self._color_h.node.branch()
        else:
            self.node_color = self.add_branch_node_color

    
    def add_hierarchy_node_color(self):
        '''
        Increases the shade of each level of nodes in relation to depth.
        '''
        if self.node_color == self.add_hierarchy_node_color:
            return self._color_h.node.hierarchy()
        else:
            self.node_color = self.add_hierarchy_node_color


    # ---------------------- Edge Color ----------------------
    def add_branch_edge_color(self):
        '''
        Each branch from the root node is a different color.
        '''
        if self.edge_color == self.add_branch_edge_color:
            return self._color_h.edge.branch()
        else:
            self.edge_color = self.add_branch_edge_color

    def add_hierarchy_edge_color(self):
        '''
        Each increases shade of edge as depth increases.
        '''
        if self.edge_color == self.add_hierarchy_edge_color:
            return self._color_h.edge.hierarchy()
        else:
            self.edge_color = self.add_hierarchy_edge_color

    # ---------------------- Node Size ----------------------
    def add_hierarchy_node_size(self):
        '''
        Each level from the root node is smaller than parent.
        '''
        if self.node_size == self.add_hierarchy_node_size:
            return self._size_h.hierarchy()
        else:
            self.node_size = self.add_hierarchy_node_size

    # ---------------------- Node Size ----------------------
    def add_logic_node_shape(self):
        '''
        Sets shapes based on logical operators (OR/AND) specified within OWL ontology.
        '''
        if self.node_shape == self.add_logic_node_shape:
            return self._shape_h.node.logical()
        else:
            self.node_shape = self.add_logic_node_shape
