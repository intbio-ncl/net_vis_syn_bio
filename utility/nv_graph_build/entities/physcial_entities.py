from entities.entity import Entity
from entities.requirement import *

class PhysicalEntity(Entity):
    def __init__(self,disjoint=True,requirements=[]):
        super().__init__(disjoint,requirements)  

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
        r = requirements + [PromoterRoleRequirement()]
        super().__init__(requirements=r)

class RBS(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [RBSRoleRequirement()]
        super().__init__(requirements=r)  

class CDS(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [CDSRoleRequirement()]
        super().__init__(requirements=r)  

class Terminator(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [TerminatorRoleRequirement()]
        super().__init__(requirements=r)  

class Gene(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [GeneRoleRequirement()]
        super().__init__(requirements=r)  

class Operator(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [OperatorRoleRequirement()]
        super().__init__(requirements=r)  

class EngineeredRegion(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [EngineeredRegionRoleRequirement()]
        super().__init__(requirements=r)

class EngineeredTag(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [EngineeredTagRoleRequirement()]
        super().__init__(requirements=r)

class StartCodon(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [StartCodonRoleRequirement()]
        super().__init__(requirements=r)

class Tag(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [TagRoleRequirement()]
        super().__init__(requirements=r)

class NonCovBindingSite(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [NonCovBindingSiteRoleRequirement()]
        super().__init__(requirements=r)

class EngineeredGene(DNA):
    def __init__(self,requirements=[]):
        r = requirements + [EngineeredGeneRoleRequirement()]
        super().__init__(requirements=r)

# -------------- Complex --------------
class Complex(PhysicalEntity):
    def __init__(self,requirements=[]):
        r = requirements + [ComplexRoleRequirement()]
        super().__init__(requirements=r)  

# -------------- Protein --------------
class Protein(PhysicalEntity):
    def __init__(self,requirements=[]):
        r = requirements + [PromoterRoleRequirement()]
        super().__init__(requirements=r)  

class TranscriptionFactor(Protein):
    def __init__(self,requirements=[]):
        r = requirements + [TranscriptionFactorRoleRequirement()]
        super().__init__(requirements=r)  

# -------------- RNA --------------
class RNA(PhysicalEntity):
    def __init__(self,requirements=[]):
        r = requirements + [RNARoleRequirement()]
        super().__init__(requirements=r)  

class mRNA(RNA):
    def __init__(self,requirements=[]):
        r = requirements + [mRNARoleRequirement()]
        super().__init__(requirements=r)  

class sgRNA(RNA):
    def __init__(self,requirements=[]):
        r = requirements + [sgRNARoleRequirement()]
        super().__init__(requirements=r)  

# -------------- Small Molecule --------------
class SmallMolecule(PhysicalEntity):
    def __init__(self,requirements=[]):
        r = requirements + [SmallMoleculeRoleRequirement()]
        super().__init__(requirements=r)  

class Effector(SmallMolecule):
    def __init__(self,requirements=[]):
        r = requirements + [EffectorRoleRequirement()]
        super().__init__(requirements=r)  