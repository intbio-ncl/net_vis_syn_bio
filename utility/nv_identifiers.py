from rdflib import URIRef, RDF

class KnowledgeGraphIdentifiers:
    def __init__(self):
        self.namespaces = Namespace()
        self.objects = Objects(self.namespaces)
        self.predicates = Predicates(self.namespaces)
    
class Namespace:  
    def __init__(self):
        identifiers = URIRef('http://identifiers.org/')
        self.sequence_ontology = URIRef(identifiers + 'so/SO:')
        self.sbo_biomodels = URIRef(identifiers + 'biomodels.sbo/SBO:') 
        self.chebi = URIRef(identifiers + 'chebi/CHEBI:') 
        self.go = URIRef(identifiers + 'go/GO:') 
        self.biopax = URIRef('http://www.biopax.org/release/biopax-level3.owl#')
        self.dc = URIRef('http://purl.org/dc/terms/')
        self.edam = URIRef('http://edamontology.org/format')
        self.nv = URIRef('http://knowledge_graph/')

class Predicates:
    def __init__(self, namespaces):
        self.namespaces = namespaces
        self.rdf_type = URIRef(RDF.type)
        self.role = URIRef(self.namespaces.nv + "role")
        self.input = URIRef(self.namespaces.nv + "input")
        self.output = URIRef(self.namespaces.nv + "output")
        self.alias = URIRef(self.namespaces.dc + 'title')
        self.description = URIRef(self.namespaces.dc + 'description')

class Objects:
    def __init__(self, namespaces):
        self.namespaces = namespaces
        self.entity = URIRef(self.namespaces.nv + "Entity")
        self.descriptor = URIRef(self.namespaces.nv + "Descriptor")
        self.interaction = URIRef(self.namespaces.nv + "Interaction")

identifiers = KnowledgeGraphIdentifiers()