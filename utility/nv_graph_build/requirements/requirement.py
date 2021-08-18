from rdflib.extras.infixowl import Property
from property.property import Property,Role,HasCharacteristic

class Requirement:
    def __init__(self,property):
        if not isinstance(property,Property):
            property = Property(property)
        self.property = property

class RoleRequirement(Requirement):
    def __init__(self,values):
        super().__init__(Role())
        if not isinstance(values,(list,tuple,set)):
            values = [values]
        self.values = values

class CharacteristicRequirement(Requirement):
    def __init__(self,values):
        super().__init__(HasCharacteristic())
        if not isinstance(values,(list,tuple,set)):
            values = [values]
        self.values = values