from entities.abstract_entity import PhysicalEntity
from property.protocols import HasContainer

class Container(PhysicalEntity):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            r = []
        else:
            r = equivalents
        p = properties + [HasContainer(Container)]
        super().__init__(properties=p,equivalents=r)