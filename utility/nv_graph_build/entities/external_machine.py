from entities.abstract_entity import PhysicalEntity
from equivalent import protocol_equivalent as pe

class ExternalMachine(PhysicalEntity):
    def __init__(self,equivalents=[]):
        if equivalents == []:
            r = []
        else:
            r = equivalents
        super().__init__(equivalents=r)