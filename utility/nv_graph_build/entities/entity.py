from rdflib import URIRef,RDF,OWL,RDFS,BNode
from identifiers import identifiers
class Entity:
    def __init__(self,disjoint=False,requirements=[]):
        class_name = self.__class__.__name__
        self.uri = URIRef(identifiers.namespaces.nv + class_name)
        self.disjoint = disjoint
        self.requirements = requirements




