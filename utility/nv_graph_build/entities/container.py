from entities.abstract_entity import PhysicalEntity
from property.protocols import HasContainer
from equivalent import protocol_equivalent as pe

class Container(PhysicalEntity):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            e = [pe.ContainerEquivalent()]
        else:
            e = equivalents
        p = properties + [HasContainer(Container)]
        super().__init__(properties=p,equivalents=e,restrictions=restrictions)