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
    def set_full_preset(self):
        '''
        Pre-set methods with an affinity for displaying the raw graph view.
        '''
        preset_functions = [self.set_tree_mode,
                            self.set_full_graph_view,
                            self.set_dagre_layout,
                            self.add_standard_node_color,
                            self.add_standard_edge_color,
                            self.add_node_name_labels, 
                            self.add_edge_name_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_actions_level_0_io_explicit_preset(self):
        '''
        Pre-set methods with an affinity for displaying the explicit actions view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_action_io_explicit_view,
                            self.set_dagre_layout,
                            self.add_type_node_color,
                            self.add_standard_edge_color,
                            self.add_source_dest_node_labels, 
                            self.add_edge_no_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_actions_level_1_io_aggregate_preset(self):
        '''
        Pre-set methods with an affinity for displaying the explicit actions view with aggreagted containers.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_action_io_aggregate_view,
                            self.set_dagre_layout,
                            self.add_type_node_color,
                            self.add_standard_edge_color,
                            self.add_source_dest_node_labels, 
                            self.add_edge_no_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_actions_level_2_flow_preset(self):
        '''
        Pre-set methods with an affinity for displaying the standard actions view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_action_flow_view,
                            self.set_dagre_layout,
                            self.add_type_node_color,
                            self.add_standard_edge_color,
                            self.add_explicit_source_dest_node_labels, 
                            self.add_edge_no_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_actions_level_3_io_implicit_preset(self):
        '''
        Pre-set methods with an affinity for displaying the implicit actions view..
        '''
        preset_functions = [self.set_network_mode,
                            self.set_action_io_implicit_view,
                            self.set_dagre_layout,
                            self.add_parent_node_color,
                            self.add_object_type_edge_color,
                            self.add_node_name_labels, 
                            self.add_edge_no_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_heirarchy_preset(self):
        '''
        Pre-set methods with an affinity for displaying the heirarchy of objects and actions
        '''
        preset_functions = [self.set_network_mode,
                            self.set_heirarchy_view,
                            self.set_dagre_layout,
                            self.add_type_node_color,
                            self.add_standard_edge_color,
                            self.add_source_dest_node_labels, 
                            self.add_edge_no_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    # ---------------------- View ----------------------------------------

    def set_action_io_explicit_view(self):
        '''
        Sub graph viewing the sequential list of actions and related containers.
        '''
        if self.view == self.set_action_io_explicit_view:
            self._builder.set_action_io_explicit_view()
        else:
           self.view =self.set_action_io_explicit_view


    def set_action_io_aggregate_view(self):
        '''
        Sub graph viewing the sequential list of actions and related containers.
        '''
        if self.view == self.set_action_io_aggregate_view:
            self._builder.set_action_io_aggregate_view()
        else:
           self.view =self.set_action_io_aggregate_view

    def set_action_flow_view(self):
        '''
        Sub graph viewing the least sequenctial list of actions
        '''
        if self.view == self.set_action_flow_view:
            self._builder.set_action_flow_view()
        else:
           self.view =self.set_action_flow_view

    def set_action_io_implicit_view(self):
        '''
        Sub graph viewing the inputs and outputs of actions.
        '''
        if self.view == self.set_action_io_implicit_view:
            self._builder.set_action_io_implicit_view()
        else:
           self.view =self.set_action_io_implicit_view

    def set_heirarchy_view(self):
        '''
        Sub graph viewing heirarchy of objects/actions in protocol.
        '''
        if self.view == self.set_heirarchy_view:
            self._builder.set_heirarchy_view()
        else:
           self.view =self.set_heirarchy_view

    # ---------------------- Node Labels --------------------------------- 
    def add_source_dest_node_labels(self):
        '''
        Edge labels pertain to Inputs and Outputs of a action.
        '''
        if self.node_text == self.add_source_dest_node_labels:
            return self._label_h.node.source_dest()
        else:
            self.node_text  = self.add_source_dest_node_labels

    def add_explicit_source_dest_node_labels(self):
        '''
        Edge labels pertain to Inputs and Outputs of a action including container names.
        '''
        if self.node_text == self.add_explicit_source_dest_node_labels:
            return self._label_h.node.source_dest_explicit()
        else:
            self.node_text  = self.add_explicit_source_dest_node_labels

    def add_parent_node_labels(self):
        '''
        Edge labels pertain to parents of container and action nodes.
        '''
        if self.node_text == self.add_parent_node_labels:
            return self._label_h.node.parent()
        else:
            self.node_text  = self.add_parent_node_labels

    # ---------------------- Edge Labels ---------------------------------
    def add_process_type_edge_labels(self):
        '''
        Edge labels pertain to process where available.
        '''
        if self.edge_text == self.add_process_type_edge_labels:
            return self._label_h.edge.process_type()
        else:
            self.edge_text = self.add_process_type_edge_labels

    # ---------------------- Node Color ----------------------------------
    def add_type_node_color(self):
        '''
        Each type is mapped to a distinct color.
        '''
        if self.node_color == self.add_type_node_color:
            return self._color_h.node.nv_type()
        else:
            self.node_color = self.add_type_node_color

    def add_parent_node_color(self):
        '''
        Each parent is mapped to a color.
        '''
        if self.node_color == self.add_parent_node_color:
            return self._color_h.node.parent()
        else:
            self.node_color = self.add_parent_node_color

    # ---------------------- Edge Color ----------------------------------
    def add_object_type_edge_color(self):
        '''
        Each the class of valid edges are mapped to color.
        '''
        if self.edge_color == self.add_object_type_edge_color:
            return self._color_h.edge.object_type()
        else:
            self.edge_color = self.add_object_type_edge_color

    # ---------------------- Node Size -----------------------------------

    def add_action_node_size(self):
        '''
        Action Nodes are larger than non-action (Containers etc.)
        '''
        if self.node_size == self.add_action_node_size:
            return self._size_h.action()
        else:
            self.node_size = self.add_action_node_size
