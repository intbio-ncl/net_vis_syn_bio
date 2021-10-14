import sys,os
import math
import re

import dash_cytoscape as cyto
import networkx as nx
from networkx.algorithms.dag import dag_longest_path
from rdflib import Literal,URIRef,RDF

from util.sbol_identifiers import identifiers
from util.color_manager import StandardPalette
from util.color_manager import SBOLClassPalette
from util.color_manager import SBOLTypePalette
from util.color_manager import SBOLRolePalette
from util.color_manager import SBOLGeneticRolePalette
from util.color_manager import SBOLPredicatePalette
from util.color_manager import palette_list

from visual.abstract_visual import AbstractVisualiser
from builder.sbol_builder import SBOLBuilder

class SBOLVisualiser(AbstractVisualiser):
    def __init__(self, graph = None):
        super().__init__()
        if graph is None:
            self._graph = None
        elif isinstance(graph,SBOLBuilder):
            self._graph = graph
            self.graph_view = self._graph.graph
        else:
            self._graph = SBOLBuilder(graph)
            self.graph_view = self._graph.graph

    # ---------------------- Set Preset (Sets one or more other settings to focus on a specific thing in the graph) ----------------------
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

    def set_single_module_preset(self):
        '''
        Pre-set methods with an affinity for displaying the maps view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_single_module_view,
                            self.set_cose_layout,
                            self.add_centrality_node_size,
                            self.add_standard_edge_color,
                            self.add_class_node_color,
                            self.add_edge_no_labels,
                            self.add_node_name_labels]
        return self._set_preset(preset_functions)


    
    # ---------------------- Set Graph (Set a different graph view) ----------------------
    def set_pruned_view(self):
        '''
        Sub graph viewing the raw SBOL graph with specific edges removed 
        that are deemed not useful for visualisation.
        '''
        pruned_graph = self._graph.produce_pruned_graph()
        self.graph_view = pruned_graph

    def set_interaction_verbose_view(self):
        '''
        Sub graph viewing all interactions within the graph including explicit 
        visualisation to participants. 
        '''
        interaction_graph = self._graph.produce_interaction_verbose_graph()
        self.graph_view = interaction_graph

    def set_interaction_view(self):
        '''
        Sub graph viewing all interactions within the graph implicitly visualises 
        participants by merging interaction node and participant edges into a single edge. 
        '''
        interaction_graph = self._graph.produce_interaction_graph()
        self.graph_view = interaction_graph

    def set_genetic_interaction_view(self):
        '''
        Sub graph viewing genetic interactions within the graph.
        Abstracts proteins and non-genetic actors.
        '''
        interaction_graph = self._graph.produce_genetic_interaction_graph()
        self.graph_view = interaction_graph

    def set_protein_protein_interaction_view(self):
        '''
        Sub graph viewing interactions between proteins. Abstracts DNA + Non-genetic actors. 
        Only visulises what the effect the presence of a protein has upon other proteins.
        '''
        ppi_graph = self._graph.produce_protein_protein_interaction_graph()
        self.graph_view = ppi_graph

    def set_heirarchy_view(self):
        '''
        Sub graph viewing the design as a heirachy of entities.
        '''
        components_preset = self._graph.produce_heirarchy_graph()
        self.graph_view = components_preset

    def set_components_view(self):
        '''
        Sub graph viewing the Components both heirarchical and functional within the design.
        '''
        components_preset = self._graph.produce_components_graph()
        self.graph_view = components_preset

    def set_module_view(self):
        '''
        Sub graph viewing the connection between modules within the design.
        '''
        module_preset = self._graph.produce_module_graph()
        self.graph_view = module_preset

    def set_maps_view(self):
        '''
        Sub graph viewing both heirarchy and module views with maps between.
        '''
        maps_preset = self._graph.produce_maps_graph()
        self.graph_view = maps_preset

    def set_single_module_view(self):
        '''
        Sub graph viewing both heirarchy and module views with maps between.
        '''
        maps_preset = self._graph.produce_single_module_graph()
        self.graph_view = maps_preset
   
    # ---------------------- Pick the node content ----------------------            
    def add_node_role_labels(self):
        '''
        Textual data pertaining to a node relates to the 
        SBOL Role of the node if said node has this property.
        '''
        if self.node_text_preset == self.add_node_role_labels:
            node_texts = []
            for node in self.graph_view.nodes():
                role = self._graph.graph.get_role(node)
                if role is not None:
                    role_identifier = role[1]["key"]
                    role_name = identifiers.translate_role(role_identifier)
                    if role_name is not None:
                        node_texts.append(role_name)
                        continue

                role = self._graph.graph.get_type(node)
                if role is not None:
                    role_identifier = role[1]["key"]
                    role_name = identifiers.translate_role(role_identifier)
                    if role_name is None:
                        role_name = ""
                    node_texts.append(role_name)
                    continue

                obj_type = self._graph.graph.get_rdf_type(node)
                if obj_type is None:
                    node_texts.append("No Type")
                    continue
                else:
                    obj_name = self._get_name(str(obj_type[1]["key"]))
                    node_texts.append(obj_name)
            
            return node_texts
        else:
            self.node_text_preset = self.add_node_role_labels


    # ---------------------- Pick the node color ----------------------
    def add_class_node_color(self):
        '''
        Each SBOL class is set to a unique color i.e. a color per object rdf-type.
        '''
        if self.node_color_preset == self.add_class_node_color:
            colors = []
            for node,data in self.graph_view.nodes(data=True):
                node_type = self._graph.graph.get_rdf_type(node)
                if node_type is not None:
                    rdf_type = node_type[1]["key"]
                    rdf_name = self._get_name(rdf_type)
                    colors.append({rdf_name : SBOLClassPalette[rdf_type].value})
                else:
                    colors.append({"property" : SBOLClassPalette.default.value})
            return colors
        else:
            self.node_color_preset = self.add_class_node_color

    def add_type_node_color(self):
        '''
        Each SBOL type is given a unique color i.e. a color per SBOL type.
        '''
        if self.node_color_preset == self.add_type_node_color:
            colors = []
            for node,data in self.graph_view.nodes(data=True):
                node_type = self._graph.graph.get_type(node)
                if node_type is None:
                    colors.append({"no_type" : SBOLTypePalette.default.value})
                    continue
                else:
                    node_type = node_type[1]["key"]
                    node_type_name = self._translate_role(node_type)
                    colors.append({node_type_name : SBOLTypePalette[node_type].value})
            return colors
        else:
            self.node_color_preset = self.add_type_node_color

    def add_role_node_color(self):
        '''
        Each SBOL type is given a distinct number, 
        each role of said type is given a shade of that color.
        '''
        if self.node_color_preset == self.add_role_node_color:
            colors = []
            for node,data in self.graph_view.nodes(data=True):
                node_type = self._graph.graph.get_type(node)
                if node_type is None:
                    color = {"no_type" : SBOLTypePalette.default.value}
                else:
                    node_role = self._graph.graph.get_role(node)
                    node_type = node_type[1]["key"]
                    try:
                        node_role = node_role[1]["key"]
                        node_type_name = self._translate_role(node_role)
                        color = {node_type_name : SBOLRolePalette[node_type].value[node_role].value}
                    except (KeyError,TypeError):
                        node_type_name = self._translate_role(node_type)
                        color = {node_type_name : SBOLTypePalette[node_type].value}
                colors.append(color)
            return colors
        else:
            self.node_color_preset = self.add_role_node_color

    def add_genetic_node_color(self):
        '''
        Each SBOL role ascociated with genetic/DNA entities are given a color.
        '''
        if self.node_color_preset == self.add_genetic_node_color:
            colors = []
            dna_types = [identifiers.external.component_definition_DNA,
                         identifiers.external.component_definition_DNARegion]

            for node,data in self.graph_view.nodes(data=True):
                node_type = self._graph.graph.get_type(node)
                if node_type is None or node_type[1]["key"] not in dna_types:
                    color = {"no_type" : SBOLGeneticRolePalette.default.value}
                else:
                    node_role = self._graph.graph.get_role(node)
                    node_type = node_type[1]["key"]
                    try:
                        node_role = node_role[1]["key"]
                        node_type_name = self._translate_role(node_role)
                        color = {node_type_name : SBOLGeneticRolePalette[node_role].value}
                    except (KeyError,TypeError):
                        node_type_name = self._translate_role(node_type)
                        color = {node_type_name : SBOLGeneticRolePalette.default.value}
                colors.append(color)
            return colors
        else:
            self.node_color_preset = self.add_genetic_node_color

    def add_hierarchy_node_color(self):
        '''
        Each level of heirarchy has a colour.
        '''
        if self.node_color_preset == self.add_hierarchy_node_color:
            colors = []
            for node,data in self.graph_view.nodes(data=True):
                rdf_type = self._graph.graph.get_rdf_type(node)
                if rdf_type is None:
                    colors.append({"primary" : StandardPalette.primary.value})
                    continue
                rdf_type = rdf_type[1]["key"]
                if rdf_type in identifiers.objects.top_levels:
                    colors.append({"secondary" : StandardPalette.secondary.value})
                else:
                    colors.append({"tertiary" : StandardPalette.tertiary.value})
            return colors
        else:
            self.node_color_preset = self.add_hierarchy_node_color

    def add_gradient_node_color(self):
        '''
        Adds color gradient to graph where closer nodes are similar colors.
        '''
        if self.node_color_preset == self.add_gradient_node_color:
            color_map = {}
            longest_path = dag_longest_path(self.graph_view._graph)
            for node in longest_path:
                node_data = self.graph_view.nodes[node]
            colors = []
            for node,data in self.graph_view.nodes(data=True):
                colors.append({node : color_map[node]})
            return colors
        else:
            self.node_color_preset = self.add_gradient_node_color

    def add_collection_node_color(self):
        '''
        Nodes are grouped into collections and has colours based on collection.
        '''
        if self.node_color_preset == self.add_collection_node_color:
            color_map = {}
            palette_index = 0
            top_levels = self._graph._graph.get_top_levels()
            for node,data in top_levels:
                if node not in self.graph_view.nodes:
                    continue
                if palette_index >= len(palette_list) -1 :
                    palette_index = 0
                color_map[node] = palette_list[palette_index]
                palette_index +=1
            colors = []

            for node,data in self.graph_view.nodes(data=True):
                if node in color_map.keys():
                    node_name = self._get_name(data["key"])
                    colors.append({node_name : color_map[node]})
                else:
                    p_node = self._graph._find_nearest_object(node,self.graph_view,
                                                        identifiers.objects.top_levels)
                    p_node_name = self._get_name(self._graph.nodes[p_node]["key"])
                    colors.append({p_node_name : color_map[p_node]})
            return colors
        else:
            self.node_color_preset = self.add_collection_node_color


    # ---------------------- Set Node Size ----------------------
    def add_hierarchy_node_size(self):
        '''
        The lower a node in the graph as a heirachy the smaller the node.
        '''
        if self.node_size_preset == self.add_hierarchy_node_size:
            node_sizes = []
            for node,data in self.graph_view.nodes(data=True):
                rdf_type = self._graph.graph.get_rdf_type(node)
                if rdf_type is None:
                    node_sizes.append(self._standard_node_size/2)
                    continue
                rdf_type = rdf_type[1]["key"]
                if rdf_type in identifiers.objects.top_levels:
                    node_sizes.append(self._standard_node_size*2)
                else:
                    node_sizes.append(self._standard_node_size)
            return node_sizes
        else:
            self.node_size_preset = self.add_hierarchy_node_size


    # ---------------------- Set Edge Color --------------------
    def add_class_edge_color(self):
        '''
        A static color set for common/interesting SBOL predicates.
        Note, not all predicates given color as number of predicates greater 
        than number of distinguishable colors.
        '''
        if self.edge_color_preset == self.add_class_edge_color:
            edge_colors = []
            for n,v,e in self.graph_view.edges(keys=True):
                predicate = e[1]
                try:
                    edge_name = self._get_name(predicate)
                    edge_color = {edge_name : SBOLPredicatePalette[predicate].value}
                except KeyError:
                    edge_color = {"default" : SBOLPredicatePalette.default.value}

                edge_colors.append(edge_color)
            return edge_colors       
        else:
            self.edge_color_preset = self.add_class_edge_color


    def add_type_edge_color(self):
        '''
        Color for each Interaction predicate.
        '''
        if self.edge_color_preset == self.add_type_edge_color:
            edge_colors = []
            for n,v,e in self.graph_view.edges(keys=True):
                predicate = e[1]
                try:
                    edge_name = self._translate_role(predicate)
                    edge_color = {edge_name : SBOLTypePalette[predicate].value}
                except KeyError:
                    edge_color = {"no_type" : SBOLTypePalette.default.value}

                edge_colors.append(edge_color)
            return edge_colors       
        else:
            self.edge_color_preset = self.add_type_edge_color

    


    def _translate_role(self,identifier):
        node_type_name = identifiers.translate_role(identifier)
        if node_type_name is None:
            node_type_name = self._get_name(identifier)
        node_type_name = node_type_name.replace(" ","_").lower()
        return node_type_name