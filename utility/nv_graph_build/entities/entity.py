from rdflib import URIRef
from nv_identifiers import identifiers

class Entity:
    def __init__(self,class_name):
        self.uri = URIRef()