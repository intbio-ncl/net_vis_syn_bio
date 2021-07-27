from visual.abstract_visual import AbstractVisualiser
from builder.knowledge_builder import KnowledgeBuilder
from util.color_manager import KGClassPalette

class KnowledgeVisualiser(AbstractVisualiser):
    def __init__(self, graph = None):
        super().__init__()
        if graph is None:
            self._graph = None
        elif isinstance(graph,KnowledgeBuilder):
            self._graph = graph
            self.graph_view = self._graph.graph
        else:
            self._graph = KnowledgeBuilder(graph)
            self.graph_view = self._graph.graph
    

    def set_synonyms_preset(self):
        '''
        Pre-set methods with an affinity for displaying the synonyms view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_synonyms_view,
                            self.set_cose_bilkent_layout,
                            self.add_standard_node_size,
                            self.add_class_node_color,
                            self.add_edge_no_labels,
                            self.add_node_name_labels]
        return self._set_preset(preset_functions)

    def set_interactions_preset(self):
        '''
        Pre-set methods with an affinity for displaying the interactions view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_interaction_view,
                            self.set_cola_layout,
                            self.add_standard_node_size,
                            self.add_standard_node_color,
                            self.add_edge_name_labels,
                            self.add_node_name_labels,
                            self.set_bezier_edge_shape
                            ]
        return self._set_preset(preset_functions)

    def set_entity_preset(self):
        '''
        Pre-set methods with an affinity for displaying the entity view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_entity_view,
                            self.set_cose_layout,
                            self.add_class_node_color,
                            self.add_node_name_labels,
                            self.add_standard_node_size,
                            self.add_edge_no_labels]
        return self._set_preset(preset_functions)

    def set_interaction_type_preset(self):
        '''
        Pre-set methods with an affinity for displaying the interaction type view.
        '''
        preset_functions = [self.set_network_mode,
                            self.set_interaction_type_view,
                            self.set_klay_layout,
                            self.add_node_name_labels,
                            self.add_centrality_node_size,
                            self.add_standard_node_color,
                            self.add_edge_no_labels,
                            self.add_standard_edge_color]
        return self._set_preset(preset_functions)
    

    def set_synonyms_view(self):
        '''
        Sub graph viewing all entities with related synonyms in knowledge graph.
        '''
        synonym_graph = self._graph.produce_synonym_graph()
        self.graph_view = synonym_graph

    def set_interaction_view(self):
        '''
        Sub graph viewing all known interactions between biological 
        entites within the knowledge graph.
        '''
        interaction_graph = self._graph.produce_interaction_graph()
        self.graph_view = interaction_graph
    
    def set_interaction_type_view(self):
        '''
        Sub graph viewing all known interactions types and 
        what are the typical inputs/outputs.
        '''
        interaction_type_graph = self._graph.produce_interaction_type_graph()
        self.graph_view = interaction_type_graph

    def set_entity_view(self):
        '''
        Sub graph viewing all known biological entties with 
        their known roles and aliases.
        '''
        entity_graph = self._graph.produce_entity_graph()
        self.graph_view = entity_graph


    # ---------------------- Pick the node color ----------------------
    def add_class_node_color(self):
        '''
        Each Knowledge Graph class is set to a unique color 
        i.e. a color per object rdf-type.
        '''
        if self.node_color_preset == self.add_class_node_color:
            colors = []
            for node,data in self.graph_view.nodes(data=True):
                node_type = self._graph.graph.get_rdf_type(node)
                if node_type is not None:
                    rdf_type = node_type[1]["key"]
                    rdf_name = self._get_name(rdf_type)
                    colors.append({rdf_name : KGClassPalette[rdf_type].value})
                else:
                    colors.append({"default" : KGClassPalette.default.value})
            return colors
        else:
            self.node_color_preset = self.add_class_node_color

