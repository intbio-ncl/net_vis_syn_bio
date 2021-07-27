from rdflib import URIRef, RDF

class KnowledgeGraphIdentifiers:
    def __init__(self):
        self.namespaces = Namespace()
        self.objects = Objects(self.namespaces)
        self.predicates = Predicates(self.namespaces)
    
class KnowledgeGraphNamespaces:
    def __init__(self):
        self.base = URIRef('http://knowledge_graph/')
        self.entity = URIRef(self.base + "entity/")
        self.interaction = URIRef(self.base + "interaction/")

class Namespace:  
    def __init__(self):
        
        self.knowledge_graph = KnowledgeGraphNamespaces()
        identifiers = URIRef('http://identifiers.org/')
        self.sequence_ontology = URIRef(identifiers + 'so/SO:')
        self.sbo_biomodels = URIRef(identifiers + 'biomodels.sbo/SBO:') 
        self.chebi = URIRef(identifiers + 'chebi/CHEBI:') 
        self.go = URIRef(identifiers + 'go/GO:') 

        self.biopax = URIRef('http://www.biopax.org/release/biopax-level3.owl#')
        self.dc = URIRef('http://purl.org/dc/terms/')
        self.edam = URIRef('http://edamontology.org/format')

class Predicates:
    def __init__(self, namespaces):
        self.namespaces = namespaces
        self.rdf_type = URIRef(RDF.type)
        self.role = URIRef(self.namespaces.knowledge_graph.entity + "role")
        self.predicate_map = URIRef(self.namespaces.knowledge_graph.interaction + "predicate")
        self.mask = URIRef(self.namespaces.knowledge_graph.base + "mask")

        self.inhibition = URIRef(self.namespaces.knowledge_graph.interaction + "inhibition")
        self.stimulation = URIRef(self.namespaces.knowledge_graph.interaction + "stimulation")
        self.biochemical_reaction = URIRef(self.namespaces.knowledge_graph.interaction + "biochemical_reaction")
        self.noncovalent_bonding = URIRef(self.namespaces.knowledge_graph.interaction + "noncovalent_bonding")
        self.degradation = URIRef(self.namespaces.knowledge_graph.interaction + "degradation")
        self.genetic_production = URIRef(self.namespaces.knowledge_graph.interaction + "genetic_production")
        self.control = URIRef(self.namespaces.knowledge_graph.interaction + "control")

        self.alias = URIRef(self.namespaces.dc + 'title')
        self.description = URIRef(self.namespaces.dc + 'description')

        self.interaction_subject = URIRef(self.namespaces.knowledge_graph.interaction + "subject")
        self.interaction_object = URIRef(self.namespaces.knowledge_graph.interaction + "object")

        self.interactions = [self.inhibition,
                            self.stimulation,
                            self.biochemical_reaction,
                            self.noncovalent_bonding,
                            self.degradation,
                            self.genetic_production,
                            self.control]

class Objects:
    def __init__(self, namespaces):
        self.namespaces = namespaces

        self.entity_type = URIRef(self.namespaces.knowledge_graph.base + "Entity")
        self.descriptor_type = URIRef(self.namespaces.knowledge_graph.base + "Descriptor")

        self.DNA = URIRef(self.namespaces.biopax + "Dna")
        self.DNARegion = URIRef(self.namespaces.biopax + "DnaRegion")
        self.RNA = URIRef(self.namespaces.biopax + "Rna")
        self.RNARegion = URIRef(self.namespaces.biopax + "RnaRegion")
        self.protein = URIRef(self.namespaces.biopax + "Protein")
        self.smallMolecule = URIRef(self.namespaces.biopax + "SmallMolecule")
        self.complex = URIRef(self.namespaces.biopax + "Complex")

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
        self.startCodon     = URIRef(self.namespaces.sequence_ontology + "0000318")
        self.tag            = URIRef(self.namespaces.sequence_ontology + "0000324")
        self.engineeredTag  = URIRef(self.namespaces.sequence_ontology + "0000807")
        self.sgRNA          = URIRef(self.namespaces.sequence_ontology + "0001998")
        self.transcriptionFactor = URIRef(self.namespaces.go + "0003700")
        self.effector       = URIRef(self.namespaces.chebi + "35224") 

        self.inhibitor = URIRef(self.namespaces.sbo_biomodels + "0000020")
        self.inhibited = URIRef(self.namespaces.sbo_biomodels + "0000642")
        self.stimulator =  URIRef(self.namespaces.sbo_biomodels + "0000459")
        self.stimulated = URIRef(self.namespaces.sbo_biomodels + "0000643")
        self.modifier = URIRef(self.namespaces.sbo_biomodels + "0000019")
        self.modified = URIRef(self.namespaces.sbo_biomodels + "0000644")
        self.reactant = URIRef(self.namespaces.sbo_biomodels + "0000010")
        self.product = URIRef(self.namespaces.sbo_biomodels + "0000011")
        self.gp_promoter = URIRef(self.namespaces.sbo_biomodels + "0000598") 
        self.template = URIRef(self.namespaces.sbo_biomodels + "0000645")

        self.inhibition = URIRef(self.namespaces.sbo_biomodels + "0000169")
        self.stimulation = URIRef(self.namespaces.sbo_biomodels + "0000170")
        self.biochemical_reaction = URIRef(self.namespaces.sbo_biomodels + "0000176")
        self.noncovalent_bonding = URIRef(self.namespaces.sbo_biomodels + "0000177")
        self.degradation = URIRef(self.namespaces.sbo_biomodels + "0000179")
        self.genetic_production = URIRef(self.namespaces.sbo_biomodels + "0000589")
        self.control = URIRef(self.namespaces.sbo_biomodels + "0000168")

identifiers = KnowledgeGraphIdentifiers()