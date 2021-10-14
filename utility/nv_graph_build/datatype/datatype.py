from rdflib import URIRef
from identifiers import identifiers

class Datatype:
    def __init__(self,name=None):
        if name is None:
            name = self.__class__.__name__
        self.uri = URIRef(identifiers.namespaces.nv + name)

class Input(Datatype):
    def __init__(self):
        super().__init__()

class Output(Datatype):
    def __init__(self):
        super().__init__()