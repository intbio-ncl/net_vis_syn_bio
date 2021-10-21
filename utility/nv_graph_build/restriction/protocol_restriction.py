from restriction.abstract_restriction import RoleRestriction
from identifiers import identifiers

class ExtractRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.extract]
        super().__init__(values)

class DispenseRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.dispense]
        super().__init__(values)

class TransferRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.transfer]
        super().__init__(values)

class ConsolidateRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.consolidate]
        super().__init__(values)

class DistributeRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.distribute]
        super().__init__(values)

class ContainerRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.container]
        super().__init__(values)

class InstrumentRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.instrument]
        super().__init__(values)

class PipetteRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.pipette]
        super().__init__(values)

class ProtocolRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.protocol]
        super().__init__(values)

class ExternalMachineRestriction(RoleRestriction):
    def __init__(self):
        values = [identifiers.roles.external_machine]
        super().__init__(values)
