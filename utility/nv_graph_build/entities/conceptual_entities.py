from entities.entity import Entity
from requirements import conceptual_requirement as ce

class ConceptualEntity(Entity):
    def __init__(self,disjoint=True,properties=[],requirements=[]):
        super().__init__(disjoint,properties=properties,requirements=requirements)  

class Reaction(ConceptualEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = []
        else:
            r = requirements
        super().__init__(requirements=r)

class Translation(Reaction):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ce.TranslationRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Transcription(Reaction):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ce.TranscriptionRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Degradation(Reaction):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ce.DegradationRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class NonCovalentBonding(Reaction):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ce.NonCovBondingRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Dissociation(Reaction):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ce.DissociationRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Hydrolysis(Dissociation):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ce.HydrolysisRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)




class Interaction(ConceptualEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = []
        else:
            r = requirements
        super().__init__(requirements=r)

class Activation(Interaction):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ce.ActivationRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Repression(Interaction):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ce.RepressionRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class GeneticProduction(Interaction):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ce.GeneticProductionRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)