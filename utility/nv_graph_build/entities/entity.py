from rdflib import URIRef
from identifiers import identifiers
from property.property import PartOf

default_properties = [PartOf]
class Entity:
    def __init__(self,disjoint=False,properties=[],requirements=[]):
        class_name = self.__class__.__name__
        self.uri = URIRef(identifiers.namespaces.nv + class_name)
        self.disjoint = disjoint
        self.properties = [p(Entity) for p in default_properties] + properties
        self.requirements = requirements



    @classmethod
    def uri(cls):
        return URIRef(identifiers.namespaces.nv + cls.__name__) 