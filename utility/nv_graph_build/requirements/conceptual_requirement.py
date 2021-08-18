from requirements.requirement import RoleRequirement
from identifiers import identifiers

class TranslationRoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.translation]
        super().__init__(values)

class TranscriptionRoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.transcription]
        super().__init__(values)

class DegradationRoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.degradation]
        super().__init__(values)

class NonCovBondingRoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.noncovalent_bonding]
        super().__init__(values)

class DissociationRoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.dissociation]
        super().__init__(values)

class HydrolysisRoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.hydrolysis]
        super().__init__(values)

class ActivationRoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.stimulation]
        super().__init__(values)

class RepressionRoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.inhibition]
        super().__init__(values)

class GeneticProductionRoleRequirement(RoleRequirement):
    def __init__(self):
        values = [identifiers.roles.genetic_production]
        super().__init__(values)