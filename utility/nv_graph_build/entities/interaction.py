from entities.abstract_entity import ConceptualEntity
from equivalent import interaction_equivalent as ce
from restriction import recipe_restriction as rr

class Interaction(ConceptualEntity):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            equiv = []
        else:
            equiv = equivalents
        if restrictions == []:
            res = []
        else:
            res = restrictions
        p = properties + []
        super().__init__(properties=p,
        equivalents=equiv,restrictions=res)

class Activation(Interaction):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            equiv = [ce.ActivationRoleEquivalent()]
        else:
            equiv = equivalents
        if restrictions == []:
            res = [rr.ActivationRecipe()]
        else:
            res = restrictions
        super().__init__(properties=properties,
        equivalents=equiv,restrictions=res)

class Repression(Interaction):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            equiv = [ce.RepressionRoleEquivalent()]
        else:
            equiv = equivalents
        if restrictions == []:
            res = [rr.RepressionRecipe()]
        else:
            res = restrictions
        super().__init__(properties=properties,
        equivalents=equiv,restrictions=res)

class GeneticProduction(Interaction):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            equiv = [ce.GeneticProductionRoleEquivalent()]
        else:
            equiv = equivalents
        if restrictions == []:
            res = [rr.GeneticProductionRecipe()]
        else:
            res = restrictions
        super().__init__(properties=properties,
        equivalents=equiv,restrictions=res)



