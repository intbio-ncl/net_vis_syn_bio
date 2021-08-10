from rdflib import URIRef
from identifiers import identifiers
from entities.property import PartOf

default_properties = [PartOf]
class Entity:
    def __init__(self,disjoint=False,properties=[],requirements=[]):
        class_name = self.__class__.__name__
        self.uri = URIRef(identifiers.namespaces.nv + class_name)
        self.disjoint = disjoint
        self.properties = [p() for p in default_properties] + properties
        self.requirements = requirements




