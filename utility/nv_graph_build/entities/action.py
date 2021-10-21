from entities.abstract_entity import ConceptualEntity
from entities.container import Container
from restriction import action_recipes as ar
from property.property import ConsistsOf
from property import actions as ap
from equivalent import protocol_equivalent as pe

class Action(ConceptualEntity):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        p = properties + [ConsistsOf(Action)]
        super().__init__(properties=p,equivalents=equivalents,
                        restrictions=restrictions)

class Extract(Action): # Source
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            e = [pe.ExtractEquivalent()]
        else:
            e = equivalents
        p = properties + [ap.Source(Container)]
        super().__init__(properties=p,equivalents=e,
                        restrictions=restrictions)

class Dispense(Action): # Location
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            e = [pe.DispenseEquivalent()]
        else:
            e = equivalents
        p = properties + [ap.Destination(Container)]
        super().__init__(properties=p,equivalents=e,
                        restrictions=restrictions)

class Transfer(Action): # Source - Location
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            e = [pe.TransferEquivalent()]
        else:
            e = equivalents
        r = restrictions + [ar.TransferRecipe()]
        super().__init__(properties=properties,equivalents=e,
                        restrictions=r)

class Consolidate(Action):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            e = [pe.ConsolidateEquivalent()]
        else:
            e = equivalents
        super().__init__(properties=properties,equivalents=e,
                        restrictions=restrictions)

class Distribute(Action):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            e = [pe.DistributeEquivalent()]
        else:
            e = equivalents
        super().__init__(properties=properties,equivalents=e,
                        restrictions=restrictions)

