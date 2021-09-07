from restriction.physcial_restriction import PhyscialCharacteristicRestriction
class Equivalent:
    def __init__(self,restrictions=[]):
        self.restrictions = restrictions

class PhysicalEquivalent(Equivalent):
    def __init__(self,restrictions=[]):
        if restrictions == []:
            r = [PhyscialCharacteristicRestriction()]
        else:
            r = restrictions
        super().__init__(r)
        
class ConceptualEquivalent(Equivalent):
    def __init__(self,restrictions=[]):
        super().__init__(restrictions) 
