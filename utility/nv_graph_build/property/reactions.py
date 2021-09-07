from property.property import Property
from property.property import Direction
from datatype.datatype import Input,Output

class ReactionProperty(Property):
    def __init__(self,range,properties=[]):
        super().__init__(range,properties=properties)

class Reactant(ReactionProperty):
    def __init__(self,range):
        p = [Direction(Input())]
        super().__init__(range,p)

class Product(ReactionProperty):
    def __init__(self,range):
        p = [Direction(Output())]
        super().__init__(range,p)

class Template(ReactionProperty):
    def __init__(self,range):
        p = [Direction(Input())]
        super().__init__(range,p)
