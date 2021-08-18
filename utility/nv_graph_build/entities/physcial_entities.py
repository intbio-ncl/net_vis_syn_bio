from entities.entity import Entity
from requirements import physcial_requirement as pr

class PhysicalEntity(Entity):
    def __init__(self,disjoint=True,properties=[],requirements=[]):
        super().__init__(disjoint,properties=properties,requirements=requirements)  

# -------------- DNA --------------
class DNA(PhysicalEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.PhyscialCharacteristicRequirement(),
                pr.DNARoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Promoter(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.PromoterRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class RBS(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.RBSRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)


class CDS(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.CDSRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Terminator(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.TerminatorRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Gene(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.GeneRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Operator(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.OperatorRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class EngineeredRegion(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.EngineeredRegionRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class EngineeredTag(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.EngineeredTagRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class StartCodon(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.StartCodonRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class Tag(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.TagRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class NonCovBindingSite(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.NonCovBindingSiteRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class EngineeredGene(DNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.EngineeredGeneRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

# -------------- Complex --------------
class Complex(PhysicalEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.PhyscialCharacteristicRequirement(),
                pr.ComplexRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

# -------------- Protein --------------
class Protein(PhysicalEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.PhyscialCharacteristicRequirement(),
                pr.ProteinRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class TranscriptionFactor(Protein):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.TranscriptionFactorRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

# -------------- RNA --------------
class RNA(PhysicalEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.PhyscialCharacteristicRequirement(),
                pr.RNARoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class mRNA(RNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.mRNARoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

class sgRNA(RNA):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.sgRNARoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)

# -------------- Small Molecule --------------
class SmallMolecule(PhysicalEntity):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.PhyscialCharacteristicRequirement(),
                pr.SmallMoleculeRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)  

class Effector(SmallMolecule):
    def __init__(self,requirements=[]):
        if requirements == []:
            r = [pr.EffectorRoleRequirement()]
        else:
            r = requirements
        super().__init__(requirements=r)