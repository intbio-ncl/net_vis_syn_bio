from rdflib import URIRef
from identifiers import identifiers
from property.property import PartOf
from equivalent.abstract_equivalent import PhysicalEquivalent

default_properties = []
class Entity:
    def __init__(self,disjoint=False,properties=[],equivalents=[],restrictions=[]):
        class_name = self.__class__.__name__
        self.uri = URIRef(identifiers.namespaces.nv + class_name)
        self.disjoint = disjoint
        self.properties = [p(Entity) for p in default_properties] + properties
        self.equivalents = equivalents
        self.restrictions = restrictions

    @classmethod
    def uri(cls):
        return URIRef(identifiers.namespaces.nv + cls.__name__) 

class PhysicalEntity(Entity):
    def __init__(self,disjoint=True,properties=[],equivalents=[],restrictions=[]):
        p = properties + [PartOf(PhysicalEntity)]
        if equivalents == []:
            equiv = [PhysicalEquivalent()]
        else:
            equiv = equivalents
        super().__init__(disjoint,properties=p,
        equivalents=equiv,restrictions=restrictions)  
        
class ConceptualEntity(Entity):
    def __init__(self,disjoint=True,properties=[],equivalents=[],restrictions=[]):
        super().__init__(disjoint,properties=properties,
        equivalents=equivalents,restrictions=restrictions)  