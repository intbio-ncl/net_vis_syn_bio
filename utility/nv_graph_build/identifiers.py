from rdflib import URIRef,RDF

class Identifiers:
    def __init__(self):
        self.namespaces = Namespace()
        self.predicates = Predicates(self.namespaces)
        self.roles = Roles(self.namespaces)
    
class Namespace:
    def __init__(self):
        identifiers = URIRef('http://identifiers.org/')
        self.nv = URIRef("http://www.nv_ontology.org/")
        self.sequence_ontology = URIRef(identifiers + 'so/SO:')
        self.sbo_biomodels = URIRef(identifiers + 'biomodels.sbo/SBO:') 
        self.identifier_edam = URIRef(identifiers + 'edam/')
        self.biopax = URIRef('http://www.biopax.org/release/biopax-level3.owl#')
        self.dc = URIRef('http://purl.org/dc/terms/')
        self.edam = URIRef('http://edamontology.org/format')
        self.prov = URIRef('http://www.w3.org/ns/prov#')

class Predicates:
    def __init__(self, namespaces):
        self.namespaces = namespaces
        self.rdf_type = URIRef(RDF.type)

class Roles:
    def __init__(self, namespaces):
        self.namespaces = namespaces

        self.physical_entity = URIRef(self.namespaces.biopax + "PhysicalEntity")
        self.conceptual_entity = URIRef(self.namespaces.biopax + "Interaction") # This tag isn't great.

        self.DNA = URIRef(self.namespaces.biopax + "Dna")
        self.DNARegion = URIRef(self.namespaces.biopax + "DnaRegion")
        self.RNA = URIRef(self.namespaces.biopax + "Rna")
        self.RNARegion = URIRef(self.namespaces.biopax + "RnaRegion")
        self.protein = URIRef(self.namespaces.biopax + "Protein")
        self.smallMolecule = URIRef(self.namespaces.biopax + "SmallMolecule")
        self.complex = URIRef(self.namespaces.biopax + "Complex")
        self.all = URIRef("www.placeholder.com/all_type")

        self.promoter       = URIRef(self.namespaces.sequence_ontology + "0000167")
        self.rbs            = URIRef(self.namespaces.sequence_ontology + "0000139")
        self.cds            = URIRef(self.namespaces.sequence_ontology + "0000316")
        self.terminator     = URIRef(self.namespaces.sequence_ontology + "0000141")
        self.gene           = URIRef(self.namespaces.sequence_ontology + "0000704")
        self.operator       = URIRef(self.namespaces.sequence_ontology + "0000057")
        self.engineeredGene = URIRef(self.namespaces.sequence_ontology + "0000280")
        self.mRNA           = URIRef(self.namespaces.sequence_ontology + "0000234")
        self.engineeredRegion = URIRef(self.namespaces.sequence_ontology + "0000804")
        self.nonCovBindingSite = URIRef(self.namespaces.sequence_ontology + "0001091")
        self.effector       = URIRef("http://identifiers.org/chebi/CHEBI:35224") 
        self.startCodon     = URIRef(self.namespaces.sequence_ontology + "0000318")
        self.tag            = URIRef(self.namespaces.sequence_ontology + "0000324")
        self.engineeredTag  = URIRef(self.namespaces.sequence_ontology + "0000807")
        self.sgRNA          = URIRef(self.namespaces.sequence_ontology + "0001998")
        self.transcriptionFactor = URIRef("http://identifiers.org/go/GO:0003700")

        self.inhibition = URIRef(self.namespaces.sbo_biomodels + "0000169")
        self.stimulation = URIRef(self.namespaces.sbo_biomodels + "0000170")
        self.biochemical_reaction = URIRef(self.namespaces.sbo_biomodels + "0000176")
        self.noncovalent_bonding = URIRef(self.namespaces.sbo_biomodels + "0000177")
        self.degradation = URIRef(self.namespaces.sbo_biomodels + "0000179")
        self.genetic_production = URIRef(self.namespaces.sbo_biomodels + "0000589")
        self.control = URIRef(self.namespaces.sbo_biomodels + "0000168")

        self.inhibitor = URIRef(self.namespaces.sbo_biomodels + "0000020")
        self.inhibited = URIRef(self.namespaces.sbo_biomodels + "0000642")
        self.stimulator =  URIRef(self.namespaces.sbo_biomodels + "0000459")
        self.stimulated = URIRef(self.namespaces.sbo_biomodels + "0000643")
        self.modifier = URIRef(self.namespaces.sbo_biomodels + "0000019")
        self.modified = URIRef(self.namespaces.sbo_biomodels + "0000644")
        self.product = URIRef(self.namespaces.sbo_biomodels + "0000011")
        self.reactant = URIRef(self.namespaces.sbo_biomodels + "0000010")
        self.participation_promoter = URIRef(self.namespaces.sbo_biomodels + "0000598") 
        self.template = URIRef(self.namespaces.sbo_biomodels + "0000645")

        self.translation = URIRef(self.namespaces.sbo_biomodels + "0000184")
        self.transcription = URIRef(self.namespaces.sbo_biomodels + "0000183")
        self.dissociation = URIRef(self.namespaces.sbo_biomodels + "0000180")
        self.hydrolysis = URIRef(self.namespaces.sbo_biomodels + "0000376")



identifiers = Identifiers()