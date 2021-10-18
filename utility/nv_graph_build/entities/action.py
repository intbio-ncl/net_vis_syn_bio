from entities.abstract_entity import ConceptualEntity
from entities.container import Container
from restriction import action_recipes as ar
from property.property import ConsistsOf
from property import actions as ap

class Action(ConceptualEntity):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        p = properties + [ConsistsOf(Action)]
        super().__init__(properties=p,equivalents=equivalents,
                        restrictions=restrictions)

class Extract(Action): # Source
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        p = properties + [ap.Source(Container)]
        super().__init__(properties=p,equivalents=equivalents,
                        restrictions=restrictions)

class Dispense(Action): # Location
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        p = properties + [ap.Destination(Container)]
        super().__init__(properties=p,equivalents=equivalents,
                        restrictions=restrictions)

class Transfer(Action): # Source - Location
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if restrictions == []:
            res = [ar.TransferRecipe()]
        else:
            res = restrictions
        super().__init__(properties=properties,equivalents=equivalents,
                        restrictions=res)

class Consolidate(Action):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        super().__init__(properties=properties,equivalents=equivalents,
                        restrictions=restrictions)

class Distribute(Action):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        super().__init__(properties=properties,equivalents=equivalents,
                        restrictions=restrictions)

