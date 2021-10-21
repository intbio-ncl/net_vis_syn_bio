from equivalent.abstract_equivalent import ConceptualEquivalent
from equivalent.abstract_equivalent import PhysicalEquivalent
from restriction import protocol_restriction as pr

class ExtractEquivalent(ConceptualEquivalent):
    def __init__(self):
        restrictions = [pr.ExtractRestriction()]
        super().__init__(restrictions)

class DispenseEquivalent(ConceptualEquivalent):
    def __init__(self):
        restrictions = [pr.DispenseRestriction()]
        super().__init__(restrictions)

class TransferEquivalent(ConceptualEquivalent):
    def __init__(self):
        restrictions = [pr.TransferRestriction()]
        super().__init__(restrictions)

class ConsolidateEquivalent(ConceptualEquivalent):
    def __init__(self):
        restrictions = [pr.ConsolidateRestriction()]
        super().__init__(restrictions)

class DistributeEquivalent(ConceptualEquivalent):
    def __init__(self):
        restrictions = [pr.DistributeRestriction()]
        super().__init__(restrictions)

class ContainerEquivalent(PhysicalEquivalent):
    def __init__(self):
        restrictions = [pr.ContainerRestriction()]
        super().__init__(restrictions)

class InstrumentEquivalent(PhysicalEquivalent):
    def __init__(self):
        restrictions = [pr.InstrumentRestriction()]
        super().__init__(restrictions)

class PipetteEquivalent(PhysicalEquivalent):
    def __init__(self):
        restrictions = [pr.PipetteRestriction()]
        super().__init__(restrictions)

class ProtocolEquivalent(PhysicalEquivalent):
    def __init__(self):
        restrictions = [pr.ProtocolRestriction()]
        super().__init__(restrictions)

class ExternalMachineEquivalent(PhysicalEquivalent):
    def __init__(self):
        restrictions = [pr.ExternalMachineRestriction()]
        super().__init__(restrictions)