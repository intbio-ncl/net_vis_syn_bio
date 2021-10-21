from entities.abstract_entity import PhysicalEntity
from equivalent import protocol_equivalent as pe

class ExternalMachine(PhysicalEntity):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            e = [pe.ExternalMachineEquivalent()]
        else:
            e = equivalents
        super().__init__(equivalents=e)