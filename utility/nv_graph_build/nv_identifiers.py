from rdflib import URIRef, RDF

class KnowledgeGraphIdentifiers:
    def __init__(self):
        self.namespaces = Namespace()
        self.objects = Objects(self.namespaces)
        self.predicates = Predicates(self.namespaces)
        self.roles = Roles(self.namespaces)
    
class Namespace:  
    def __init__(self):
        self.nv = URIRef('http://nv_ontology/')
        identifiers = URIRef('http://identifiers.org/')
        self.sequence_ontology = URIRef(identifiers + 'so/SO:')
        self.sbo_biomodels = URIRef(identifiers + 'biomodels.sbo/SBO:') 
        self.identifier_edam = URIRef(identifiers + 'edam/')
        self.biopax = URIRef('http://www.biopax.org/release/biopax-level3.owl#')

class Predicates:
    def __init__(self, namespaces):
        self.namespaces = namespaces
        self.rdf_type = URIRef(RDF.type)
        self.role = URIRef(self.namespaces.nv + "role")
        self.contains = URIRef(self.namespaces.nv + "contains")

class Objects:
    def __init__(self, namespaces):
        self.namespaces = namespaces
        self.entity = URIRef(self.namespaces.nv + "Entity")
        self.descriptor = URIRef(self.namespaces.nv + "Descriptor")
        self.interaction = URIRef(self.namespaces.nv + "Interaction")

class Roles:
    def __init__(self,namespaces):
        self.DNA = URIRef(namespaces.biopax + "Dna")
        self.DNARegion = URIRef(namespaces.biopax + "DnaRegion")
        self.RNA = URIRef(namespaces.biopax + "Rna")
        self.RNARegion = URIRef(namespaces.biopax + "RnaRegion")
        self.protein = URIRef(namespaces.biopax + "Protein")
        self.smallMolecule = URIRef(namespaces.biopax + "SmallMolecule")
        self.complex = URIRef(namespaces.biopax + "Complex")

        self.promoter       = URIRef(namespaces.sequence_ontology + "0000167")
        self.rbs            = URIRef(namespaces.sequence_ontology + "0000139")
        self.cds            = URIRef(namespaces.sequence_ontology + "0000316")
        self.terminator     = URIRef(namespaces.sequence_ontology + "0000141")
        self.gene           = URIRef(namespaces.sequence_ontology + "0000704")
        self.operator       = URIRef(namespaces.sequence_ontology + "0000057")
        self.engineeredGene = URIRef(namespaces.sequence_ontology + "0000280")
        self.mRNA           = URIRef(namespaces.sequence_ontology + "0000234")
        self.engineeredRegion = URIRef(namespaces.sequence_ontology + "0000804")
        self.nonCovBindingSite = URIRef(namespaces.sequence_ontology + "0001091")
        self.effector       = URIRef("http://identifiers.org/chebi/CHEBI:35224") 
        self.startCodon     = URIRef(namespaces.sequence_ontology + "0000318")
        self.tag            = URIRef(namespaces.sequence_ontology + "0000324")
        self.engineeredTag  = URIRef(namespaces.sequence_ontology + "0000807")
        self.sgRNA          = URIRef(namespaces.sequence_ontology + "0001998")
        self.transcriptionFactor = URIRef("http://identifiers.org/go/GO:0003700")

identifiers = KnowledgeGraphIdentifiers()