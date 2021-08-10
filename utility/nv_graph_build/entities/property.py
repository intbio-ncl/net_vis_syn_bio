from identifiers import identifiers

class Property:
    def __init__(self,property):
        self.property = property
    
    def __repr__(self):
        return f'{self.property}'

class Role(Property):
    def __init__(self):
        super().__init__(identifiers.predicates.role)

class PartOf(Property):
    def __init__(self):
        super().__init__(identifiers.predicates.partOf)