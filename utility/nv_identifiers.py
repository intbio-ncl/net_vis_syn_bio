from rdflib import URIRef, RDF

class KnowledgeGraphIdentifiers:
    def __init__(self):
        self.namespaces = Namespace()
        self.objects = Objects(self.namespaces)
        self.predicates = Predicates(self.namespaces)
        self.external = External(self.namespaces)
    
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
        self.nv = URIRef('http://nv_ontology/')

class Predicates:
    def __init__(self, namespaces):
        self.namespaces = namespaces
        self.rdf_type = URIRef(RDF.type)

        self.role = URIRef(self.namespaces.nv + "role")
        self.contains = URIRef(self.namespaces.nv + "contains")
        
        self.alias = URIRef(self.namespaces.dc + 'title')
        self.description = URIRef(self.namespaces.dc + 'description')

class Objects:
    def __init__(self, namespaces):
        self.namespaces = namespaces
        self.entity = URIRef(self.namespaces.nv + "Entity")
        self.descriptor = URIRef(self.namespaces.nv + "Descriptor")
        self.interaction = URIRef(self.namespaces.nv + "Interaction")

class External:
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

        self.inhibition = URIRef(namespaces.sbo_biomodels + "0000169")
        self.stimulation = URIRef(namespaces.sbo_biomodels + "0000170")
        self.biochemical_reaction = URIRef(namespaces.sbo_biomodels + "0000176")
        self.noncovalent_bonding = URIRef(namespaces.sbo_biomodels + "0000177")
        self.degradation = URIRef(namespaces.sbo_biomodels + "0000179")
        self.genetic_production = URIRef(namespaces.sbo_biomodels + "0000589")
        self.control = URIRef(namespaces.sbo_biomodels + "0000168")

        self.inhibitor = URIRef(namespaces.sbo_biomodels + "0000020")
        self.inhibited = URIRef(namespaces.sbo_biomodels + "0000642")
        self.stimulator =  URIRef(namespaces.sbo_biomodels + "0000459")
        self.stimulated = URIRef(namespaces.sbo_biomodels + "0000643")
        self.modifier = URIRef(namespaces.sbo_biomodels + "0000019")
        self.modified = URIRef(namespaces.sbo_biomodels + "0000644")
        self.product = URIRef(namespaces.sbo_biomodels + "0000011")
        self.reactant = URIRef(namespaces.sbo_biomodels + "0000010")
        self.participation_promoter = URIRef(namespaces.sbo_biomodels + "0000598") 
        self.template = URIRef(namespaces.sbo_biomodels + "0000645")

identifiers = KnowledgeGraphIdentifiers()