import os
import re
import json

import dash_cytoscape as cyto
cyto.load_extra_layouts()
from builder.builder import NVBuilder
from visual.handlers.layout import LayoutHandler
from visual.handlers.label import LabelHandler
from visual.handlers.color import ColorHandler
from visual.handlers.size import SizeHandler
from visual.handlers.shape import ShapeHandler

default_stylesheet_fn = os.path.join(os.path.dirname(os.path.realpath(__file__)),"default_stylesheet.txt")

class NVisualiser:
    def __init__(self,graph=None):
        if graph is None:
            self._builder = None
        elif isinstance(graph,NVBuilder):
            self._builder = graph
        else:
            self._builder = NVBuilder(graph)

        self._layout_h = LayoutHandler()
        self._label_h = LabelHandler()
        self._color_h = ColorHandler()
        self._size_h = SizeHandler()
        self._shape_h = ShapeHandler()

        self.pos = []
        self.view = self.set_full_graph_view
        self.mode = self.set_network_mode
        self.layout = self.set_spring_layout
        self.node_text = self.add_node_no_labels
        self.edge_text = self.add_edge_no_labels
        self.node_color = self.add_standard_node_color
        self.edge_color = self.add_standard_edge_color
        self.node_size = self.add_standard_node_size
        self.node_shape = self.set_circle_node_shape
        self.edge_shape = self.set_straight_edge_shape()
        self.default_stylesheet = self._build_default_stylesheet()

    def copy_settings(self):
        current_settings = [
            self.layout,
            self.node_text,
            self.edge_text,
            self.node_color,
            self.edge_color,
            self.node_size,
            self.node_shape]
        return current_settings
    
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
    def set_full_graph_view(self):
        '''
        Renders the Full graph. 
        '''
        if self.view == self.set_full_graph_view:
            self._builder.set_full_view()
        else:
           self.view =self.set_full_graph_view

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

    # ---------------------- View Mode ------------------------------------
    def set_network_mode(self):
        '''
        Set the graph to the standard Node-Edge-Node Network graph.
        Duplicates are merged into the same node leading to connectedness.
        '''
        if self.mode == self.set_network_mode:
            self._builder.set_network_mode()
        else:
            self.mode = self.set_network_mode

    def set_tree_mode(self):
        '''
        Produce a Tree-Like graph where duplicates within 
        the graph are NOT treated as the same node.
        This will result in a tree/heirarchy structure within a graph.
        '''
        if self.mode == self.set_tree_mode:
            self._builder.set_tree_mode()
        else:
            self.mode = self.set_tree_mode

# ---------------------- Pick a layout ----------------------
    def set_spring_layout(self):
        '''
        Position nodes using Fruchterman-Reingold force-directed algorithm.
        '''
        if self.layout == self.set_spring_layout:
            self.pos = self._layout_h.spring(self._builder.view._graph)
        else:
            self.layout = self.set_spring_layout

    def set_circular_layout(self):
        '''
        Position nodes on a circle.
        '''
        if self.layout == self.set_circular_layout:
            self.pos = self._layout_h.circular(self._builder.view._graph)
        else:
            self.layout = self.set_circular_layout

    def set_kamada_kawai_layout(self):
        '''
        Position nodes using Kamada-Kawai path-length cost-function.
        '''
        if self.layout == self.set_kamada_kawai_layout:
            self.pos = self._layout_h.kamada_kawai(self._builder.view._graph)
        else:
            self.layout = self.set_kamada_kawai_layout

    def set_planar_layout(self):
        '''
        Position nodes without edge intersections.
        '''
        if self.layout == self.set_planar_layout:
            self.pos = self._layout_h.planar(self._builder.view._graph)
        else:
            self.layout = self.set_planar_layout

    def set_no_layout(self):
        '''
        No new positional data produced for graph.
        '''
        if self.layout == self.set_no_layout:
            self.pos = []
            return self._layout_h.none()
        else:
            self.layout = self.set_no_layout

    def set_concentric_layout(self):
        '''
        Position nodes into concentric circles, 
        based on the specified metric. 
        '''
        if self.layout == self.set_concentric_layout:
            self.pos = []
            return self._layout_h.concentric()
        else:
            self.layout = self.set_concentric_layout

    def set_breadthfirst_layout(self):
        '''
        Positions nodes in levels, according to the levels 
        generated by running a breadth-first search on the graph.
        '''
        if self.layout == self.set_breadthfirst_layout:
            self.pos = []
            return self._layout_h.breadthfirst()
        else:
            self.layout = self.set_breadthfirst_layout

    def set_cose_layout(self):
        '''
        Positions nodes based on the CoSE: Compound Spring Embedder - 
        A force directed layout scheme.
        '''
        if self.layout == self.set_cose_layout:
            self.pos = []
            return self._layout_h.cose()
        else:
            self.layout = self.set_cose_layout

    def set_cose_bilkent_layout(self):
        '''
        Positions nodes based on the CoSE: Compound Spring Embedder - 
        A force directed layout scheme.
        Similar to COSE but more expensive + can provide better results.
        '''
        if self.layout == self.set_cose_bilkent_layout:
            self.pos = []
            return self._layout_h.cose_bilkent()
        else:
            self.layout = self.set_cose_bilkent_layout

    def set_cola_layout(self):
        '''
        Positions nodes based on a force directed algorithm.
        '''
        if self.layout == self.set_cola_layout:
            self.pos = []
            return self._layout_h.cola()
        else:
            self.layout = self.set_cola_layout

    def set_euler_layout(self):
        '''
        Positions nodes based on a force directed algorithm.
        It is fairly fast. However, cola tends to give better results.
        '''
        if self.layout == self.set_euler_layout:
            self.pos = []
            return self._layout_h.euler()
        else:
            self.layout = self.set_euler_layout

    def set_spread_layout(self):
        '''
        Positions nodes based on a force directed algorithm.
        First, it runs cose and then it spreads out the graph 
        to fill out the viewport as much as possible.
        '''
        if self.layout == self.set_spread_layout:
            self.pos = []
            return self._layout_h.spread()
        else:
            self.layout = self.set_spread_layout

    def set_dagre_layout(self):
        '''
        Positions nodes based on a traditional binary tree heirarchical layout.
        '''
        if self.layout == self.set_dagre_layout:
            self.pos = []
            return self._layout_h.dagre()
        else:
            self.layout = self.set_dagre_layout

    def set_klay_layout(self):
        '''
        Positions nodes based on a heirarchical layout.
        '''
        if self.layout == self.set_klay_layout:
            self.pos = []
            return self._layout_h.klay()
        else:
            self.layout = self.set_klay_layout
   
    def set_grid_layout(self):
        '''
        Positions nodes based on a heirarchical layout.
        '''
        if self.layout == self.set_grid_layout:
            self.pos = []
            return self._layout_h.grid()
        else:
            self.layout = self.set_grid_layout
    
    # ---------------------- Node Labels ----------------------
    def add_node_no_labels(self):
        '''
        Textual data pertaining to a node is not rendered.
        '''
        if self.node_text == self.add_node_no_labels:
            return self._label_h.node.none(self._builder)
        else:
            self.node_text = self.add_node_no_labels

    def add_node_adjacency_labels(self):
        '''
        Textual data pertaining to a node relates 
        to number of incoming and outgoing edges.
        '''
        if self.node_text == self.add_node_adjacency_labels:
            return self._label_h.node.adjacency(self._builder)
        else:
            self.node_text = self.add_node_adjacency_labels

    def add_node_name_labels(self):
        '''
        Textual data pertaining to a node relates to the 
        name the node was provided during building of the graph.
        '''
        if self.node_text == self.add_node_name_labels:
            return self._label_h.node.name(self._builder)
        else:
            self.node_text = self.add_node_name_labels

    def add_node_type_labels(self):
        '''
        Textual data pertaining to a node is of the RDF type.
        '''
        if self.node_text == self.add_node_type_labels:
            return self._label_h.node.class_type(self._builder)
        else:
            self.node_text = self.add_node_type_labels

    def add_node_role_labels(self):
        '''
        Textual data pertaining to a node relates to the 
        Role of the node if said node has this property.
        '''
        if self.node_text == self.add_node_role_labels:
            return self._label_h.node.role(self._builder)
        else:
            self.node_text = self.add_node_role_labels

    # ---------------------- Edge Labels ----------------------
    def add_edge_no_labels(self):
        '''
        Textual data pertaining to a egde is not rendered.
        '''
        if self.edge_text == self.add_edge_no_labels:
            return self._label_h.edge.none(self._builder)
        else:
            self.edge_text = self.add_edge_no_labels

    def add_edge_name_labels(self):
        '''
        Textual data pertaining relates to the 
        name provides when building the graph.
        '''
        if self.edge_text == self.add_edge_name_labels:
            return self._label_h.edge.name(self._builder)
        else:
            self.edge_text = self.add_edge_name_labels

    # ---------------------- Node Color ----------------------
    def add_standard_node_color(self):
        '''
        All node colors are the same standard color.
        '''
        if self.node_color == self.add_standard_node_color:
            return self._color_h.node.standard(self._builder)
        else:
            self.node_color = self.add_standard_node_color

    def add_rdf_type_node_color(self):
        '''
        Di-color, Objects and Properties have a unique color.
        '''
        if self.node_color == self.add_rdf_type_node_color:
            return self._color_h.node.rdf_type(self._builder)
        else:
            self.node_color = self.add_rdf_type_node_color

    def add_class_node_color(self):
        '''
        Each class is set to a unique color i.e. a color per object rdf-type.
        '''
        if self.node_color == self.add_class_node_color:
            return self._color_h.node.nv_class(self._builder)
        else:
            self.node_color = self.add_class_node_color
    
    def add_role_node_color(self):
        '''
        Each SBOL type is given a distinct number, 
        each role of said type is given a shade of that color.
        '''
        if self.node_color == self.add_role_node_color:
            return self._color_h.node.role(self._builder)
        else:
            self.node_color = self.add_role_node_color

    # ---------------------- Edge Color ----------------------
    def add_standard_edge_color(self):
        '''
        The color pertaining to each edge is uniform. 
        '''
        if self.edge_color == self.add_standard_edge_color:
            return self._color_h.edge.standard(self._builder)
        else:
            self.edge_color = self.add_standard_edge_color

    def add_predicate_edge_color(self):
        '''
        A static color set for common/interesting SBOL predicates.
        Note, not all predicates given color as number of predicates greater 
        than number of distinguishable colors.
        '''
        if self.edge_color == self.add_predicate_edge_color:
            return self._color_h.edge.predicate(self._builder)
        else:
            self.edge_color = self.add_predicate_edge_color

    def add_interaction_edge_color(self):
        '''
        Color for each Interaction predicate.
        '''
        if self.edge_color == self.add_interaction_edge_color:
            return self._color_h.edge.interaction(self._builder)
        else:
            self.edge_color = self.add_interaction_edge_color

    # ---------------------- Node Size ----------------------
    def add_standard_node_size(self):
        '''
        The Node size for each node is equal.
        '''
        if self.node_size == self.add_standard_node_size:
            return self._size_h.standard(self._builder)
        else:
            self.node_size = self.add_standard_node_size

    def add_rdf_type_node_size(self):
        '''
        The Node size for each node is based on whether it is 
        a Object or a property i.e. does the node has an RDF type.
        '''
        if self.node_size == self.add_rdf_type_node_size:
            return self._size_h.class_type(self._builder)
        else:
            self.node_size = self.add_rdf_type_node_size

    def add_centrality_node_size(self):
        '''
        The Node size is greater the more 
        incoming + outgoing edges of said node. 
        '''
        if self.node_size == self.add_centrality_node_size:
            return self._size_h.centrality(self._builder)
        else:
            self.node_size = self.add_centrality_node_size


    def add_in_centrality_node_size(self):
        '''
        The Node size is greater the more 
        incoming edges of said node. 
        '''
        if self.node_size == self.add_in_centrality_node_size:
            return self._size_h.in_centrality(self._builder)
        else:
            self.node_size = self.add_in_centrality_node_size


    def add_out_centrality_node_size(self):
        '''
        The Node size is greater the more 
        outgoing edges of said node. 
        '''
        if self.node_size == self.add_out_centrality_node_size:
            return self._size_h.out_centrality(self._builder)
        else:
            self.node_size = self.add_out_centrality_node_size

    def add_hierarchy_node_size(self):
        '''
        The lower a node in the graph as a heirachy the smaller the node.
        '''
        if self.node_size == self.add_hierarchy_node_size:
            return self._size_h.hierarchy(self._builder)
        else:
            self.node_size = self.add_hierarchy_node_size


    # ---------------------- Node Shape ----------------------
    def set_adaptive_node_shape(self):
        '''
        Sets the shape of each node based on the RDF type of given node.
        '''
        if self.node_shape == self.set_adaptive_node_shape:
            return self._shape_h.node.adaptive(self._builder)
        else:
            self.node_shape = self.set_adaptive_node_shape

    def set_circle_node_shape(self):
        '''
        Sets the shape of each node to a circle.
        '''
        if self.node_shape == self.set_circle_node_shape:
            return self._shape_h.node.circle(self._builder)
        else:
            self.node_shape = self.set_circle_node_shape

    def set_square_node_shape(self):
        '''
        Sets the shape of each node to a square.
        '''
        if self.node_shape == self.set_square_node_shape:
            return self._shape_h.node.square(self._builder)
        else:
            self.node_shape = self.set_square_node_shape

    def set_triangle_node_shape(self):
        '''
        Sets the shape of each node to a triangle.
        '''
        if self.node_shape == self.set_triangle_node_shape:
            return self._shape_h.node.triangle(self._builder)
        else:
            self.node_shape = self.set_triangle_node_shape

    def set_rectangle_node_shape(self):
        '''
        Sets the shape of each node to a rectangle.
        '''
        if self.node_shape == self.set_rectangle_node_shape:
            return self._shape_h.node.rectangle(self._builder)
        else:
            self.node_shape = self.set_rectangle_node_shape

    def set_diamond_node_shape(self):
        '''
        Sets the shape of each node to a diamond.
        '''
        if self.node_shape == self.set_diamond_node_shape:
            return self._shape_h.node.diamond(self._builder)
        else:
            self.node_shape = self.set_diamond_node_shape

    def set_hexagon_node_shape(self):
        '''
        Sets the shape of each node to a hexagon.
        '''
        if self.node_shape == self.set_hexagon_node_shape:
            return self._shape_h.node.hexagon(self._builder)
        else:
            self.node_shape = self.set_hexagon_node_shape

    def set_octagon_node_shape(self):
        '''
        Sets the shape of each node to a octagon.
        '''
        if self.node_shape == self.set_octagon_node_shape:
            return self._shape_h.node.octagon(self._builder)
        else:
            self.node_shape = self.set_octagon_node_shape
            
    def set_vee_node_shape(self):
        '''
        Sets the shape of each node to a vee.
        '''
        if self.node_shape == self.set_vee_node_shape:
            return self._shape_h.node.vee(self._builder)
        else:
            self.node_shape = self.set_vee_node_shape

    # ---------------------- Edge Shape ----------------------
    def set_straight_edge_shape(self):
        '''
        Sets the shape of each edge to a straight line.
        '''
        self.edge_shape = self._shape_h.edge.straight()

    def set_bezier_edge_shape(self):
        '''
        Sets the shape of each edge to a straight line.
        Overlapping edges are curved.
        '''
        self.edge_shape = self._shape_h.edge.bezier()

    def set_taxi_edge_shape(self):
        '''
        Sets the shape of each edge to a two straight 
        lines with a right angle.
        '''
        self.edge_shape = self._shape_h.edge.taxi()

    def set_unbundled_bezier_edge_shape(self):
        '''
        Sets the shape of each edge based on the unbundled_bezier algorithm.
        '''
        self.edge_shape = self._shape_h.edge.unbundled_bezier()
        
    def set_loop_edge_shape(self):
        '''
        Sets the shape of each edge to a loop .
        '''
        self.edge_shape = self._shape_h.edge.loop()

    def set_haystack_edge_shape(self):
        '''
        Sets the shape of each edge based on the haystack algorithm.
        '''
        self.edge_shape = self._shape_h.edge.haystack()

    def set_segments_edge_shape(self):
        '''
        Sets the shape of each edge to a set of segments. 
        '''
        self.edge_shape = self._shape_h.edge.segments()

    def build(self,graph_id="cytoscape_graph", legend=False, width=100,height=100):
        stylesheet = self.default_stylesheet.copy()
        nodes = []
        edges = []
        node_selectors = []
        edge_selectors = []
        self.view()
        self.mode()
        node_color = self.node_color()
        node_shapes = self.node_shape()
        node_sizes = self.node_size()
        edge_color = self.edge_color()  
        node_text = self.node_text()
        edge_text = self.edge_text()
        if self.layout is not None:
            layout = self.layout()
        for index,(node,label) in enumerate(self._builder.view.nodes(data=True)):
            text = node_text[index]
            color_key = list(node_color[index].keys())[0]
            shape = node_shapes[index]
            shape = str(list(shape.values())[0])
            size = node_sizes[index]
            n_color = node_color[index][color_key]
            node,n_style = self._build_node(node,text,size,color_key,n_color,shape)
            if color_key not in node_selectors:
                stylesheet.append(n_style)    
                node_selectors.append(color_key)
            nodes.append(node)

        for index,(n,v) in enumerate(self._builder.view.edges()):
            color_key = list(edge_color[index].keys())[0]
            e_color = edge_color[index][color_key]
            edge,e_style = self._build_edge(n,v,edge_text[index],color_key,e_color)
            if color_key not in edge_selectors:
                stylesheet.append(e_style)    
                edge_selectors.append(color_key)
            edges.append(edge)

        figure = cyto.Cytoscape(id=graph_id,
                                layout=layout,
                                style={'width': f'{str(width)}vw', 'height': f'{str(height)}vh'},
                                elements=nodes + edges,
                                stylesheet = stylesheet,
                                responsive=True)

        if legend:
            legend_dict = self._build_legend(node_color,edge_color)
            return figure,legend_dict
        return figure


    def _build_node(self,n,label,size,c_key,color,shape):
        class_str = f'top-center {c_key} {shape}'
        node = {'data': {'id': n,'label': label,"size" : size},
                'classes' :class_str}
        if self.pos != []:
            n_pos = self.pos[n]
            node["position"] = {'x':2000*n_pos[0],'y':2000*n_pos[1]}
        style = {"selector" : "." + c_key, "style" : {"background-color" : color}}
        return node,style

    def _build_edge(self,n,v,label,c_key,color):
        edge = {'data': {'source': n, 'target': v, 'label': label},
                'classes' : f'center-right {c_key}'}
        style = {"selector" : "." + c_key,"style" : {"line-color" : color,
                                                    'curve-style': self.edge_shape,
                                                    "mid-target-arrow-color": color,
                                                    "mid-target-arrow-shape": "triangle"}}
        return edge,style
    

    def _build_legend(self,node_colors=[],edge_colors=[],node_shapes=[],node_sizes=[]):
        legend_dict = {}
        f_node_colors = {}
        f_edge_colors = {}
        f_node_shapes = {}
        f_node_sizes = {}
        for node_color in node_colors:
            for k,v in node_color.items():
                f_node_colors[k] = v
        if len(f_node_colors) > 0:
            legend_dict["Node Color"] = f_node_colors
        for edge_color in edge_colors:
            for k,v in edge_color.items():
                f_edge_colors[k] = v
        if len(f_edge_colors) > 0:
            legend_dict["Edge Color"] = f_edge_colors
        for node_shape in node_shapes:
            for k,v in node_shape.items():
                f_node_shapes[k] = v
        if len(f_node_shapes) > 0:
            legend_dict["Node Shape"] = f_node_shapes
        for node_size in node_sizes:
            for k,v in node_size.items():
                f_node_sizes[k] = v
        if len(f_node_sizes) > 0:
            legend_dict["Node Size"] = f_node_sizes
        return legend_dict

    def _build_default_stylesheet(self):
        with open(default_stylesheet_fn) as json_file:
            stylesheet = json.load(json_file)
        for shape in self._shape_h.node.shapes:
            stylesheet.append({
                'selector': '.' + shape,
                'style': {'shape': shape}})
        return stylesheet

    def _set_preset(self,functions):
        for func in functions:
            func()
        return functions