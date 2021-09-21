from property.property import Property
from property.property import Direction
from datatype.datatype import Input,Output
from equivalent import property_equivalent as pe

class ReactionProperty(Property):
    def __init__(self,range,properties=[],equivalents=[]):
        super().__init__(range,properties=properties,equivalents=equivalents)

class Reactant(ReactionProperty):
    def __init__(self,range):
        p = [Direction(Input())]
        e = [pe.ReactantEquivalent(),
             pe.InhibitorEquivalent(),
             pe.StimulatorEquivalent(),
             pe.PromoterEquivalent(),
             pe.ModifierEquivalent()]
        super().__init__(range,p,e)

class Product(ReactionProperty):
    def __init__(self,range):
        p = [Direction(Output())]
        e = [pe.ProductEquivalent(),
             pe.InhibitedEquivalent(),
             pe.StimulatedEquivalent(),
             pe.ModifiedEquivalent()]
        super().__init__(range,p,e)

class Template(ReactionProperty):
    def __init__(self,range):
        p = [Direction(Input())]
        e = [pe.TemplateEquivalent()]
        super().__init__(range,p,e)
