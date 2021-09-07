from restriction.abstract_restriction import RoleRestriction
from restriction.abstract_restriction import CharacteristicRestriction
from identifiers import identifiers

class ActivationRoleRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.stimulation]
        super().__init__(values)

class RepressionRoleRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.inhibition]
        super().__init__(values)

class GeneticProductionRoleRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.genetic_production]
        super().__init__(values)