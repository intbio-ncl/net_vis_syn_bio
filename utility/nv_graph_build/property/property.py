from rdflib import URIRef
from identifiers import identifiers
from datatype.datatype import Input,Output

class Property:
    def __init__(self,range=None,properties=[],default_value=None):
        name = self.__class__.__name__.lower()[0] + self.__class__.__name__[1:]
        self.property = URIRef(identifiers.namespaces.nv + name)
        if not isinstance(range, list):
            range = [range]
        self.range = range
        self.properties = properties
        self.default_value = default_value
    
    def __repr__(self):
        return f'{self.property} : {self.range}'

    def __hash__(self):
        return hash((self.property, *self.range))

    def __eq__(self, other):
        return (self.property, self.range) == (other.property, other.range)
            
class Role(Property):
    def __init__(self):
        super().__init__()

class PartOf(Property):
    def __init__(self,range):
        super().__init__(range)

class HasCharacteristic(Property):
    def __init__(self):
        super().__init__()

class ConsistsOf(Property):
    def __init__(self,range=None):
        super().__init__(range)

class Direction(Property):
    def __init__(self,value):
        r = [Input(),Output()]
        super().__init__(r,default_value=value)
    