from enum import Enum 
#from utility.nv_identifiers import identifiers 

class StandardPalette(Enum):
    primary = "#7DF5DF"
    secondary = "#86E078"
    tertiary = "#8C5EE0"
    quaternary = "#FF675D"
    final = "#FAC57D"

palette_list = [
        "#7DF5DF",
        "#86E078",
        "#8C5EE0",
        "#FF675D",
        "#FAC57D",
        "#25CCF7",
        "#CAD3C8",
        "#1B9CFC",
        "#F8EFBA",
        "#58B19F",
        "#2C3A47",
        "#B33771",
        "#3B3B98",
        "#D6A2E8",
        "#6D214F",
        "#BDC581",
        "#EAB543",
        "#FEA47F",
        "#FC427B",
        "#F97F51",]

'''
TypePalette = Enum("TypePalette",{
    identifiers.external.DNA : "#86E078",
    identifiers.external.DNARegion : "#86E078" ,
    identifiers.external.RNA : "#8C5EE0",
    identifiers.external.RNARegion : "#8C5EE0",
    identifiers.external.protein : "#FF675D",
    identifiers.external.smallMolecule : "#FAC57D",
    identifiers.external.complex : "#5779E0",

    identifiers.external.interaction_inhibition : "#87c459", 
    identifiers.external.interaction_stimulation : "#2f4f4f",
    identifiers.external.interaction_biochemical_reaction : "#F5556F",
    identifiers.external.interaction_noncovalent_bonding : "#E07747",
    identifiers.external.interaction_degradation : "#E54EF0",
    identifiers.external.interaction_genetic_production : "#d3bd4e",
    identifiers.external.interaction_control : "#DEB887",
    "default" : "#7DF5DF"
})
DNAPalette = Enum("DNAPalette",{
    identifiers.external.promoter : "#79dd69",
    identifiers.external.rbs : "#4fd23b",
    identifiers.external.cds : "#3aad28",
    identifiers.external.terminator : "#2a7f1d",
    identifiers.external.gene : "#1b5113",
    identifiers.external.engineeredGene : "#1b5113",
    identifiers.external.engineeredRegion : "#1b5113",
    identifiers.external.tag : "#64d752",
    identifiers.external.engineeredTag : "#64d752",
    identifiers.external.operator : "#8de280",
    identifiers.external.nonCovBindingSite : "#b7ecae",
    identifiers.external.startCodon : "#e0f7dc",
})
RNAPalette = Enum("RNAPalette",{
    identifiers.external.mRNA : "#b394ea",
    identifiers.external.sgRNA: "#33156b"
})
ProteinPalette = Enum("ProteinPalette",{
    identifiers.external.effector : "#ff5a50"
})
SmallMoleculePalette = Enum("SmallMoleculePalette",{
})
ComplexPalette = Enum("ComplexPalette",{
    identifiers.external.transcriptionFactor : "#a1b4ee"
})
RolePalette = Enum("RolePalette",{
    identifiers.external.DNA : DNAPalette,
    identifiers.external.DNARegion : DNAPalette,
    identifiers.external.RNA : RNAPalette,
    identifiers.external.RNARegion : RNAPalette,
    identifiers.external.protein : ProteinPalette,
    identifiers.external.smallMolecule : SmallMoleculePalette,
    identifiers.external.complex : ComplexPalette
})
GeneticRolePalette = Enum("GeneticRolePalette",{
    identifiers.external.promoter : "#86E078",
    identifiers.external.rbs : "#8C5EE0",
    identifiers.external.cds : "#FF675D",
    identifiers.external.terminator : "#FAC57D",
    identifiers.external.gene : "#5779E0",
    identifiers.external.engineeredGene : "#5779E0",
    identifiers.external.engineeredRegion : "#E54EF0",
    identifiers.external.tag : "#EBD357",
    identifiers.external.engineeredTag : "#EBD357",
    identifiers.external.operator : "#E07747",
    identifiers.external.nonCovBindingSite : "#2f4f4f",
    identifiers.external.startCodon : "#F5556F",
    "default" : "#7DF5DF"
})


ClassPalette = Enum("ClassPalette",{
    identifiers.objects.component_definition : "#b03060",
    identifiers.objects.component : "#86E078",
    identifiers.objects.module_definition : "#8C5EE0",
    identifiers.objects.functional_component : "#FF675D",
    identifiers.objects.interaction : "#FAC57D",
    identifiers.objects.sequence_annotation : "#7cfc00", 
    identifiers.objects.sequence_constraint : "#8fbc8f",
    identifiers.objects.range : "#2f4f4f",
    identifiers.objects.cut : "#add8e6",
    identifiers.objects.sequence : "#1e90ff",
    identifiers.objects.combinatorial_derivation : "#800000",
    identifiers.objects.experiment : "#808000",
    identifiers.objects.experimental_data : "#bc8f8f",
    identifiers.objects.implementation : "#ffff00",
    identifiers.objects.generic_location : "#ee82ee",
    identifiers.objects.mapsTo : "#228b22",
    identifiers.objects.module : "#ff00ff",
    identifiers.objects.model : "#8b008b",
    identifiers.objects.attachment : "#fa8072",
    identifiers.objects.collection : "#483d8b",
    identifiers.objects.participation : "#4682b4",
    identifiers.objects.activity : "#000080",
    identifiers.objects.usage : "#ff4500",
    identifiers.objects.association : "#ffa500",
    identifiers.objects.plan : "#8a2be2",
    identifiers.objects.agent : "#ff1493",
    "default" : "#7DF5DF"
}) 
PredicatePalette = Enum("PredicatePalette",{
    identifiers.predicates.component : "#b03060",
    identifiers.predicates.functional_component : "#86E078",
    identifiers.predicates.definition : "#8C5EE0",
    identifiers.predicates.type : "#FF675D",
    identifiers.predicates.role : "#FAC57D",
    identifiers.predicates.interaction : "#7cfc00",
    identifiers.predicates.participation : "#DEB887",
    identifiers.predicates.participant : "#8fbc8f",
    identifiers.predicates.sequence_annotation : "#2f4f4f",
    identifiers.predicates.sequence_constraint : "#1e90ff",
    "default" : "7DF5DF"
})
KGClassPalette = Enum("KGClassPalette",{
    kg_identifiers.objects.entity_type : "#b03060",
    kg_identifiers.objects.descriptor_type : "#86E078",
    "default" : "#7DF5DF"
}) 

'''