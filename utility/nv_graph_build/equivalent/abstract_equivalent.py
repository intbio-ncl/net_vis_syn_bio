from restriction.physcial_restriction import PhyscialCharacteristicRestriction
from restriction.conceptual_restriction import ConceptualCharacteristicRestriction

class EquivalentClass:
    def __init__(self,restrictions=[]):
        self.restrictions = restrictions

class EquivalentProperty:
    def __init__(self,equivalents):
        self.equivalents = equivalents

class PhysicalEquivalent(EquivalentClass):
    def __init__(self,restrictions=[]):
        if restrictions == []:
            r = [PhyscialCharacteristicRestriction()]
        else:
            r = restrictions
        super().__init__(r)
        
class ConceptualEquivalent(EquivalentClass):
    def __init__(self,restrictions=[]):
        if restrictions == []:
            r = [ConceptualCharacteristicRestriction()]
        else:
            r = restrictions
        super().__init__(r)

class PropertyEquivalent(EquivalentProperty):
    def __init__(self,equivalents=[]):
        super().__init__(equivalents)
