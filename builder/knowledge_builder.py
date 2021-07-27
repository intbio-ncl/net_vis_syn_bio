from rdflib import URIRef

from graphs.knowledge_graph import KnowledgeGraph
from builder.abstract_builder import AbstractBuilder
from util.kg_identifiers import identifiers

class KnowledgeBuilder(AbstractBuilder):
    def __init__(self,graph):
        super().__init__()
        self._graph = KnowledgeGraph(graph)

    def produce_synonym_graph(self):
        synonym_edges = []
        node_attrs = {}
        for n,v,e in self._graph.get_aliases():
            n_id,n_data = n
            v_id,v_data = v
            key = (n_data["key"],e[1],v_data["key"])
            edge = {"weight" : 1 ,"display_name": "alias"}
            synonym_edges.append((n_id,v_id,key,edge))
            node_attrs[n_id] = n_data
            node_attrs[v_id] = v_data
        synonyms_graph = self._graph.sub_graph(synonym_edges,node_attrs)
        return synonyms_graph
        
    def produce_interaction_graph(self):
        interaction_edges = []
        node_attrs = {}
        for n,v,e in self._graph.get_interactions():
            n_id,n_data = n
            v_id,v_data = v
            key = (n_data["key"],e[1],v_data["key"])
            edge = {"weight" : 1 ,"display_name": self.graph._get_name(e[1])}
            interaction_edges.append((n_id,v_id,e))
            node_attrs[n_id] = n_data
            node_attrs[v_id] = v_data
        interaction_graph = self._graph.sub_graph(interaction_edges,node_attrs)
        return interaction_graph
    
    def produce_interaction_type_graph(self):
        interaction_edges = []
        node_attrs = {}
        for n in self._graph.get_descriptors():
            n_id,n_data = n
            subjects = self._graph.get_subjects(n_id)
            objects = self._graph.get_objects(n_id)
            node_attrs[n_id] = n_data
            for n1,v1,e1 in subjects:
                v1_id,v1_data = v1
                node_attrs[v1_id] = v1_data
                key = (n_data["key"],e1[1],v1_data["key"])
                edge = {"weight" : 1,"display_name" : self._graph._get_name(e1[1])}
                interaction_edges.append((v1_id,n_id,key,edge))
            for n2,v2,e1 in objects:
                v2_id,v2_data = v2
                node_attrs[v2_id] = v2_data
                key = (n_data["key"],e1[1],v2_data["key"])
                edge = {"weight" : 1,"display_name" : self._graph._get_name(e1[1])}
                interaction_edges.append((n_id,v2_id,key,edge))
        interaction_graph = self._graph.sub_graph(interaction_edges,node_attrs)
        interaction_graph = self._swap_labels(interaction_graph)
        return interaction_graph

    def produce_entity_graph(self):
        entity_edges = []
        node_attrs = {}
        for n in self._graph.get_entities():
            n_id,n_data = n
            node_attrs[n_id] = n_data

            for v1_id,v1_data in self._graph.get_descriptors(n_id):
                key = (n_data["key"],identifiers.predicates.role,v1_data["key"])
                edge = {"weight" : 1,"display_name" : "Descriptor"}
                entity_edges.append((n_id,v1_id,key,edge))
                node_attrs[v1_id] = v1_data

            for n2,v2,e2 in self._graph.get_aliases(n_id):
                v2_id,v2_data = v2
                key = (n_data["key"],e2[1],v2_data["key"])
                edge = {"weight" : 1,"display_name" : "Alias"}
                entity_edges.append((n_id,v2_id,key,edge))
                node_attrs[v2_id] = v2_data
        entity_graph = self._graph.sub_graph(entity_edges,node_attrs)
        entity_graph = self._swap_labels(entity_graph)
        return entity_graph

    def _swap_labels(self,graph):
        for n1 in graph.nodes():
            d_n = graph.nodes[n1]["key"]
            if isinstance(d_n,int) or d_n.isdigit():
                graph.nodes[n1]["key"] = self._graph.get_aliases(n1)[0][1][1]["key"]
        return graph