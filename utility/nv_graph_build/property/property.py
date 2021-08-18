from identifiers import identifiers

class Property:
    def __init__(self,property,range=None):
        self.property = property
        self.range = range
    
    def __repr__(self):
        return f'{self.property} : {self.range}'

    def __hash__(self):
        return hash((self.property, self.range))

    def __eq__(self, other):
        return (self.property, self.range) == (other.property, other.range)
            

class Role(Property):
    def __init__(self):
        super().__init__(identifiers.predicates.role)

class PartOf(Property):
    def __init__(self,range):
        super().__init__(identifiers.predicates.partOf,range)

class HasCharacteristic(Property):
    def __init__(self):
        super().__init__(identifiers.predicates.hasCharacteristic)
