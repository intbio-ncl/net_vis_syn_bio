from rdflib.extras.infixowl import Property
from property.property import Property
from property.property import Role
from property.property import HasCharacteristic
from property.property import ConsistsOf

class Restriction:
    def __init__(self,property):
        if not isinstance(property,Property):
            property = Property(property)
        self.property = property

class RoleRestriction(Restriction):
    def __init__(self,values):
        super().__init__(Role())
        if not isinstance(values,(list,tuple,set)):
            values = [values]
        self.values = values

class CharacteristicRestriction(Restriction):
    def __init__(self,values):
        super().__init__(HasCharacteristic())
        if not isinstance(values,(list,tuple,set)):
            values = [values]
        self.values = values

class RecipeRestriction(Restriction):
    def __init__(self,recipe):
        super().__init__(ConsistsOf())
        self.recipe = recipe