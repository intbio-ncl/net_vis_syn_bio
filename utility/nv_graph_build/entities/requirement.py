from identifiers import identifiers

class Requirement:
    def __init__(self,property):
        self.property = property

class RoleRequirement(Requirement):
    def __init__(self,values):
        super().__init__(identifiers.predicates.role)
        if not isinstance(values,(list,tuple,set)):
            values = [values]
        self.values = values

class DNARoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.DNA,
                  identifiers.roles.DNARegion]
        super().__init__(values)

class PromoterRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.promoter)

class RBSRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.rbs)  

class CDSRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.cds)  

class TerminatorRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.terminator)  

class GeneRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.gene)  

class OperatorRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.operator)  

class EngineeredRegionRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.engineeredRegion)  

class ComplexRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.complex)  

class ProteinRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.protein)  

class TranscriptionFactorRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.transcriptionFactor)  

class EngineeredTagRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.engineeredTag)  

class StartCodonRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.startCodon)  

class TagRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.tag)  

class NonCovBindingSiteRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.nonCovBindingSite)  

class EngineeredGeneRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.engineeredGene)  
        
class RNARoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.RNA,
                  identifiers.roles.RNARegion]
        super().__init__(values)  

class RNARegionRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.RNARegion)

class mRNARoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.mRNA)  

class sgRNARoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.sgRNA)  

class SmallMoleculeRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.smallMolecule)  

class EffectorRoleRequirement(RoleRequirement):
    def __init__(self):
        super().__init__(identifiers.roles.effector)