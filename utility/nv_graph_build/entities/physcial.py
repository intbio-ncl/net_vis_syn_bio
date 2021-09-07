from entities.abstract_entity import PhysicalEntity
from equivalent import physcial_equivalent as pe

# -------------- DNA --------------
class DNA(PhysicalEntity):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.DNARoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class Promoter(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.PromoterRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class RBS(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.RBSRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)


class CDS(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.CDSRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class Terminator(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.TerminatorRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class Gene(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.GeneRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class Operator(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.OperatorRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class EngineeredRegion(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.EngineeredRegionRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class EngineeredTag(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.EngineeredTagRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class StartCodon(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.StartCodonRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class Tag(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.TagRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class NonCovBindingSite(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.NonCovBindingSiteRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class EngineeredGene(DNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.EngineeredGeneRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

# -------------- Complex --------------
class Complex(PhysicalEntity):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.ComplexRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

# -------------- Protein --------------
class Protein(PhysicalEntity):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.ProteinRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class TranscriptionFactor(Protein):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.TranscriptionFactorRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

# -------------- RNA --------------
class RNA(PhysicalEntity):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.RNARoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class mRNA(RNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.mRNARoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

class sgRNA(RNA):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.sgRNARoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)

# -------------- Small Molecule --------------
class SmallMolecule(PhysicalEntity):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.SmallMoleculeRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)  

class Effector(SmallMolecule):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = [pe.EffectorRoleEquivalent()]
        else:
            r = equivalents
        super().__init__(equivalents=r)