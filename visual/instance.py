import os

import dash_cytoscape as cyto
cyto.load_extra_layouts()
from builder.instance import InstanceBuilder
from visual.abstract import AbstractVisual

from visual.handlers.instance.layout import LayoutHandler
from visual.handlers.instance.label import LabelHandler
from visual.handlers.instance.color import ColorHandler
from visual.handlers.instance.size import SizeHandler
from visual.handlers.instance.shape import ShapeHandler

default_stylesheet_fn = os.path.join(os.path.dirname(os.path.realpath(__file__)),"default_stylesheet.txt")

class InstanceVisual(AbstractVisual):
    def __init__(self,graph=None):
        super().__init__()
        if graph is None:
            self._builder = None
        elif isinstance(graph,InstanceBuilder):
            self._builder = graph
        else:
            self._builder = InstanceBuilder(graph)

        self._layout_h = LayoutHandler()
        self._label_h = LabelHandler(self._builder)
        self._color_h = ColorHandler(self._builder)
        self._size_h = SizeHandler(self._builder)
        self._shape_h = ShapeHandler(self._builder)


        # ---------------------- Preset ------------------------------------
    def set_prune_preset(self):
        '''
        Pre-set methods with an affinity for displaying the pruned graph view.
        '''
        preset_functions = [self.set_tree_mode,
                            self.set_pruned_view,
                            self.set_cose_layout,
                            self.add_centrality_node_size,
                            self.add_class_edge_color,
                            self.add_node_name_labels,
                            self.add_edge_no_labels]
        return self._set_preset(preset_functions)

    def set_interaction_verbose_preset(self):
        '''
        Pre-set methods with an affinity for displaying the verbose interaction view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_interaction_verbose_view,
                            self.set_dagre_layout,
                            self.add_type_edge_color,
                            self.add_type_node_color,
                            self.add_edge_no_labels,
                            self.add_node_name_labels]
        return self._set_preset(preset_functions)

    def set_interaction_preset(self):
        '''
        Pre-set methods with an affinity for displaying the interaction view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_interaction_view,
                            self.set_dagre_layout,
                            self.add_type_edge_color,
                            self.add_role_node_color,
                            self.add_edge_no_labels,
                            self.add_node_name_labels]
        return self._set_preset(preset_functions)

    def set_protein_protein_interaction_preset(self):
        '''
        Pre-set methods with an affinity for displaying the ppi interaction view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_protein_protein_interaction_view,
                            self.set_dagre_layout,
                            self.add_type_edge_color,
                            self.add_standard_node_color,
                            self.add_node_name_labels,
                            self.add_edge_no_labels,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_interaction_genetic_preset(self):
        '''
        Pre-set methods with an affinity for displaying the genetic interaction view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_genetic_interaction_view,
                            self.set_dagre_layout,
                            self.add_type_edge_color,
                            self.add_genetic_node_color,
                            self.add_edge_no_labels,
                            self.add_node_name_labels,
                            self.set_bezier_edge_shape]
        return self._set_preset(preset_functions)

    def set_heirarchy_preset(self):
        '''
        Pre-set methods with an affinity for displaying the heirarchy view.
        '''
        preset_functions = [self.set_tree_mode,
                            self.set_heirarchy_view,
                            self.set_dagre_layout,
                            self.add_standard_edge_color,
                            self.add_role_node_color,
                            self.add_edge_no_labels,
                            self.add_node_name_labels]
        return self._set_preset(preset_functions)

    def set_component_preset(self):
        '''
        Pre-set methods with an affinity for displaying the component view.
        '''
        preset_functions = [self.set_tree_mode,
                            self.set_components_view,
                            self.set_cose_layout,
                            self.add_standard_edge_color,
                            self.add_centrality_node_size,
                            self.add_collection_node_color,
                            self.add_edge_no_labels,
                            self.add_node_name_labels]
        return self._set_preset(preset_functions)

    def set_module_preset(self):
        '''
        Pre-set methods with an affinity for displaying the module view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_module_view,
                            self.set_dagre_layout,
                            self.add_standard_edge_color,
                            self.add_standard_node_color,
                            self.add_edge_no_labels,
                            self.add_node_name_labels]
        return self._set_preset(preset_functions)

    def set_maps_preset(self):
        '''
        Pre-set methods with an affinity for displaying the maps view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_maps_view,
                            self.set_cose_layout,
                            self.add_centrality_node_size,
                            self.add_standard_edge_color,
                            self.add_class_node_color,
                            self.add_edge_no_labels,
                            self.add_node_name_labels]
        return self._set_preset(preset_functions)


    # ---------------------- View ------------------------------------
    def set_pruned_view(self):
        '''
        Sub graph viewing the raw graph with specific edges removed 
        that are deemed not useful for visualisation.
        '''
        if self.view == self.set_pruned_view:
            self._builder.set_pruned_view()
        else:
           self.view =self.set_pruned_view

    def set_interaction_verbose_view(self):
        '''
        Sub graph viewing all interactions within the graph including explicit 
        visualisation to participants. 
        '''
        if self.view == self.set_interaction_verbose_view:
            self._builder.set_interaction_verbose_view()
        else:
           self.view =self.set_interaction_verbose_view

    def set_interaction_view(self):
        '''
        Sub graph viewing all interactions within the graph implicitly visualises 
        participants by merging interaction node and participant edges into a single edge. 
        '''
        if self.view == self.set_interaction_view:
            self._builder.set_interaction_verbose_view()
        else:
           self.view =self.set_interaction_view
        self._builder.set_interaction_view()

    def set_genetic_interaction_view(self):
        '''
        Sub graph viewing genetic interactions within the graph.
        Abstracts proteins and non-genetic actors.
        '''
        if self.view == self.set_genetic_interaction_view:
            self._builder.set_genetic_interaction_view()
        else:
           self.view =self.set_genetic_interaction_view

    def set_protein_protein_interaction_view(self):
        '''
        Sub graph viewing interactions between proteins. Abstracts DNA + Non-genetic actors. 
        Only visulises what the effect the presence of a protein has upon other proteins.
        '''
        if self.view == self.set_protein_protein_interaction_view:
            self._builder.set_protein_protein_interaction_view()
        else:
           self.view =self.set_protein_protein_interaction_view

    def set_heirarchy_view(self):
        '''
        Sub graph viewing the design as a heirachy of entities.
        '''
        if self.view == self.set_heirarchy_view:
            self._builder.set_heirarchy_view()
        else:
           self.view =self.set_heirarchy_view

    def set_module_view(self):
        '''
        Sub graph viewing the connection between modules within the design.
        '''
        if self.view == self.set_module_view:
            self._builder.set_module_view()
        else:
           self.view =self.set_module_view
    
    # ---------------------- Node Labels ----------------------
    def add_node_role_labels(self):
        '''
        Textual data pertaining to a node relates to the 
        Role of the node if said node has this property.
        '''
        if self.node_text == self.add_node_role_labels:
            return self._label_h.node.role()
        else:
            self.node_text = self.add_node_role_labels

    # ---------------------- Edge Labels ----------------------


    # ---------------------- Node Color ----------------------  
    def add_role_node_color(self):
        '''
        Each SBOL type is given a distinct number, 
        each role of said type is given a shade of that color.
        '''
        if self.node_color == self.add_role_node_color:
            return self._color_h.node.role()
        else:
            self.node_color = self.add_role_node_color

    # ---------------------- Edge Color ----------------------
    def add_predicate_edge_color(self):
        '''
        A static color set for common/interesting SBOL predicates.
        Note, not all predicates given color as number of predicates greater 
        than number of distinguishable colors.
        '''
        if self.edge_color == self.add_predicate_edge_color:
            return self._color_h.edge.predicate()
        else:
            self.edge_color = self.add_predicate_edge_color

    def add_interaction_edge_color(self):
        '''
        Color for each Interaction predicate.
        '''
        if self.edge_color == self.add_interaction_edge_color:
            return self._color_h.edge.interaction()
        else:
            self.edge_color = self.add_interaction_edge_color

    # ---------------------- Node Size ----------------------
    def add_hierarchy_node_size(self):
        '''
        The lower a node in the graph as a heirachy the smaller the node.
        '''
        if self.node_size == self.add_hierarchy_node_size:
            return self._size_h.hierarchy()
        else:
            self.node_size = self.add_hierarchy_node_size
