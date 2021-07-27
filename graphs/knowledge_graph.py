from rdflib import URIRef
import networkx as nx

from util.kg_identifiers import identifiers
from graphs.abstract_graph import AbstractGraph

class KnowledgeGraph(AbstractGraph):
    def __init__(self,graph):
        super().__init__(graph)
        
    def get_descriptors(self,entity=None):
        if entity is not None:
            return [d[1] for d in self.search((entity,identifiers.predicates.role,None))]
        return [d[0] for d in self.search((None,identifiers.predicates.rdf_type, identifiers.objects.descriptor_type))]

    def get_entities(self,descriptor=None):
        if descriptor is not None:
            return [e[0] for e in self.search((None,identifiers.predicates.role,descriptor))]
        return [e[0] for e in self.search((None,identifiers.predicates.rdf_type,identifiers.objects.entity_type))]

    def get_aliases(self,identifier=None):
        return self.search((identifier,identifiers.predicates.alias,None))

    def get_subjects(self,descriptor=None):
        return self.search((descriptor,identifiers.predicates.interaction_subject,None))

    def get_predicates(self,descriptor=None):
        return self.search((descriptor,identifiers.predicates.predicate_map,None))

    def get_objects(self,descriptor=None):
        return self.search((descriptor,identifiers.predicates.interaction_object,None))

    def get_interactions(self,entity=None):
        return self.search((entity,identifiers.predicates.interactions,None))

    def get_interaction(self,predicate_map):
        return [a[0] for a in self.search((None,identifiers.predicates.predicate_map,predicate_map),lazy=True)]
    