from rdflib import URIRef
from nv_identifiers import identifiers

class Entity:
    def __init__(self,class_name):
        self.uri = URIRef()

class PhysicalEntity(Entity):
    def __init__(self):
        pass


# -------------- DNA --------------
class DNA(PhysicalEntity):
    def __init__(self):
        pass

class Promoter(DNA):
    def __init__(self):
        pass

class RBS(DNA):
    def __init__(self):
        pass

class CDS(DNA):
    def __init__(self):
        pass

class Terminator(DNA):
    def __init__(self):
        pass

class Gene(DNA):
    def __init__(self):
        pass

class Operator(DNA):
    def __init__(self):
        pass

class EngineeredRegion(DNA):
    def __init__(self):
        pass

# -------------- Complex --------------
class Complex(PhysicalEntity):
    def __init__(self):
        pass

# -------------- Protein --------------
class Protein(PhysicalEntity):
    def __init__(self):
        pass

class TranscriptionFactor(Protein):
    def __init__(self):
        pass

# -------------- RNA --------------
class RNA(PhysicalEntity):
    def __init__(self):
        pass

class mRNA(RNA):
    def __init__(self):
        pass

# -------------- Small Molecule --------------
class SmallMolecule(PhysicalEntity):
    def __init__(self):
        pass

class Effector(SmallMolecule):
    def __init__(self):
        pass