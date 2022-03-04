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
    def __init__(self,model,is_multiple,graph=None):
        super().__init__(is_multiple=is_multiple)
        self._builder = ProtocolBuilder(model,graph)
        self._layout_h = LayoutHandler()
        self._label_h = LabelHandler(self._builder)
        self._color_h = ColorHandler(self._builder)
        self._size_h = SizeHandler(self._builder)
        self._shape_h = ShapeHandler(self._builder)
        self._abs_level = 3
        self._detail_level = False
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

    def set_pruned_preset(self):
        '''
        Pre-set methods with an affinity for displaying the raw graph view.
        '''
        preset_functions = [self.set_tree_mode,
                            self.set_pruned_view,
                            self.set_dagre_layout,
                            self.add_type_node_color,
                            self.add_type_edge_color,
                            self.add_node_name_labels, 
                            self.add_edge_no_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_hierarchy_preset(self):
        '''
        Pre-set methods with an affinity for displaying the heirarchy of objects and actions
        '''
        preset_functions = [self.set_network_mode,
                            self.set_hierarchy_view,
                            self.set_dagre_layout,
                            self.add_type_node_color,
                            self.add_standard_edge_color,
                            self.add_node_name_labels, 
                            self.add_edge_no_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_instructions_preset(self):
        '''
        Pre-set methods with an affinity for displaying the
        instruction set.
        '''
        preset_functions = [self.set_tree_mode,
                            self.set_no_detail_level,
                            self.set_instructions_view,
                            self.set_klay_layout,
                            self.add_parent_node_color,
                            self.add_standard_edge_color,
                            self.add_node_name_labels, 
                            self.add_edge_no_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_flow_preset(self):
        '''
        Pre-set methods with an affinity for displaying flow between wells.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_flow_view,
                            self.set_dagre_layout,
                            self.add_type_node_color,
                            self.add_standard_edge_color,
                            self.add_node_name_labels, 
                            self.add_well_container_edge_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_io_preset(self):
        '''
        Pre-set methods with an affinity for displaying 
        input and outputs of actions.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_io_view,
                            self.set_klay_layout,
                            self.add_type_node_color,
                            self.add_type_edge_color,
                            self.add_well_container_node_labels, 
                            self.add_edge_no_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_process_preset(self):
        '''
        Pre-set methods with an affinity for displaying the 
        processes (actions) between wells.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_process_view,
                            self.set_klay_layout,
                            self.add_type_node_color,
                            self.add_object_type_edge_color,
                            self.add_well_container_node_labels, 
                            self.add_edge_no_labels,
                            self.add_standard_node_size,
                            self.set_circle_node_shape,
                            self.set_bezier_edge_shape,
                            self.set_no_detail_level]
        return self._set_preset(preset_functions)

    # ---------------------- View ----------------------------------------

    def set_pruned_view(self):
        '''
        Sub graph viewing the full graph with potentially redunant edges removed.
        '''
        if self.view == self.set_pruned_view:
            self._builder.set_pruned_view()
        else:
           self.view =self.set_pruned_view


    def set_hierarchy_view(self):
        '''
        Sub graph viewing heirarchy of objects/actions in protocol.
        '''
        if self.view == self.set_hierarchy_view:
            self._builder.set_hierarchy_view()
        else:
           self.view =self.set_hierarchy_view

    def set_instructions_view(self):
        '''
        Nodes:       Action | Protocol - 
        Edges:       Flow (No Model Entity) -
        Description: Flow of instructions based on linear input.
                     Edges simply dictate flow.
        '''
        if self.view == self.set_instructions_view:
            self._builder.set_instructions_view(self._abs_level,self._detail_level)
        else:
           self.view =self.set_instructions_view

    def set_flow_view(self):
        '''
        Nodes:       Action | Protocol - 
        Edges:       Well
        Description: Flow of actions based on 
                     flow of reagents between wells.
        '''
        if self.view == self.set_flow_view:
            self._builder.set_flow_view(self._abs_level,self._detail_level)
        else:
           self.view =self.set_flow_view

    def set_io_view(self):
        '''
        Nodes:       Well | Action | Protocol - 
        Edges:       input | output
        Description: Input and Output wells between actions/protocols. 
        '''
        if self.view == self.set_io_view:
            self._builder.set_io_view(self._abs_level,self._detail_level)
        else:
           self.view =self.set_io_view

    def set_process_view(self):
        '''
        Nodes:       Well - 
        Edges:       Action | Protocols -
        Description: For each action, plot physical entities and map edges actions between them. 
                     IO but Actions as edges.
        '''
        if self.view == self.set_process_view:
            self._builder.set_process_view(self._abs_level,self._detail_level)
        else:
           self.view =self.set_process_view

    def set_container_view(self):
        '''
        Displaying containers,instruments and apparatus for each protocol/action.
        '''
        if self.view == self.set_container_view:
            self._builder.set_container_view(self._detail_level)
        else:
           self.view =self.set_container_view

    # ---------------------- Detail Level ---------------------------
    def set_abstraction_level(self,level=3):
        '''
        Certain Views are capble of scaling abstraction (Level of detail).
        This slider allows certain views to be modified further.
        '''
        self._abs_level = level
        return level

    def set_no_detail_level(self):
        '''
        Certain Views are capble of providing extended data in the form of extra nodes.
        This setting disables.
        '''
        self._detail_level = False

    def set_basic_detail_level(self):
        '''
        Certain Views are capble of providing extended data in the form of extra nodes.
        This setting enables.
        '''
        self._detail_level = True

    # ---------------------- Node Labels --------------------------------- 
    def add_parent_node_labels(self):
        '''
        Edge labels pertain to parents of container and action nodes.
        '''
        if self.node_text == self.add_parent_node_labels:
            return self._label_h.node.parent()
        else:
            self.node_text  = self.add_parent_node_labels

    def add_well_container_node_labels(self):
        '''
        Well Nodes affix parent container to name. All non-well nodes have default names.
        '''
        if self.node_text == self.add_well_container_node_labels:
            return self._label_h.node.well_container()
        else:
            self.node_text  = self.add_well_container_node_labels

    # ---------------------- Edge Labels ---------------------------------
    def add_well_container_edge_labels(self):
        '''
        Well Edges affix parent container to name. All non-well edges have default names.
        '''
        if self.edge_text == self.add_well_container_edge_labels:
            return self._label_h.edge.well_container()
        else:
            self.edge_text  = self.add_well_container_edge_labels

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
