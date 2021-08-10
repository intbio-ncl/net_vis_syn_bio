from entities.entity import Entity
from entities.requirement import *

class PhysicalEntity(Entity):
    def __init__(self,disjoint=True,properties=[],requirements=[]):
        super().__init__(disjoint,properties=properties,requirements=requirements)  

# -------------- DNA --------------
class DNA(PhysicalEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [DNARoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Promoter(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [PromoterRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class RBS(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [RBSRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)


class CDS(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [CDSRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Terminator(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [TerminatorRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Gene(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [GeneRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Operator(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [OperatorRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class EngineeredRegion(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [EngineeredRegionRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class EngineeredTag(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [EngineeredTagRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class StartCodon(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [StartCodonRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Tag(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [TagRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class NonCovBindingSite(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [NonCovBindingSiteRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class EngineeredGene(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [EngineeredGeneRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

# -------------- Complex --------------
class Complex(PhysicalEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ComplexRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

# -------------- Protein --------------
class Protein(PhysicalEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [ProteinRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class TranscriptionFactor(Protein):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [TranscriptionFactorRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

# -------------- RNA --------------
class RNA(PhysicalEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [RNARoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class mRNA(RNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [mRNARoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class sgRNA(RNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [sgRNARoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

# -------------- Small Molecule --------------
class SmallMolecule(PhysicalEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [SmallMoleculeRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)  

class Effector(SmallMolecule):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [EffectorRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)