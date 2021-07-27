from enum import Enum 
from util.sbol_identifiers import identifiers
from util.kg_identifiers import identifiers as kg_identifiers


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



SBOLTypePalette = Enum("SBOLTypePalette",{
    identifiers.external.component_definition_DNA : "#86E078",
    identifiers.external.component_definition_DNARegion : "#86E078" ,
    identifiers.external.component_definition_RNA : "#8C5EE0",
    identifiers.external.component_definition_RNARegion : "#8C5EE0",
    identifiers.external.component_definition_protein : "#FF675D",
    identifiers.external.component_definition_smallMolecule : "#FAC57D",
    identifiers.external.component_definition_complex : "#5779E0",

    identifiers.external.interaction_inhibition : "#87c459", 
    identifiers.external.interaction_stimulation : "#2f4f4f",
    identifiers.external.interaction_biochemical_reaction : "#F5556F",
    identifiers.external.interaction_noncovalent_bonding : "#E07747",
    identifiers.external.interaction_degradation : "#E54EF0",
    identifiers.external.interaction_genetic_production : "#d3bd4e",
    identifiers.external.interaction_control : "#DEB887",
    "default" : "#7DF5DF"
})
SBOLDNAPalette = Enum("SBOLDNAPalette",{
    identifiers.external.component_definition_promoter : "#79dd69",
    identifiers.external.component_definition_rbs : "#4fd23b",
    identifiers.external.component_definition_cds : "#3aad28",
    identifiers.external.component_definition_terminator : "#2a7f1d",
    identifiers.external.component_definition_gene : "#1b5113",
    identifiers.external.component_definition_engineeredGene : "#1b5113",
    identifiers.external.component_definition_engineeredRegion : "#1b5113",
    identifiers.external.component_definition_tag : "#64d752",
    identifiers.external.component_definition_engineeredTag : "#64d752",
    identifiers.external.component_definition_operator : "#8de280",
    identifiers.external.component_definition_nonCovBindingSite : "#b7ecae",
    identifiers.external.component_definition_startCodon : "#e0f7dc",
})
SBOLRNAPalette = Enum("SBOLRNAPalette",{
    identifiers.external.component_definition_mRNA : "#b394ea",
    identifiers.external.component_definition_sgRNA: "#33156b"
})
SBOLProteinPalette = Enum("SBOLProteinPalette",{
    identifiers.external.component_definition_effector : "#ff5a50"
})
SBOLSmallMoleculePalette = Enum("SBOLSmallMoleculePalette",{
})
SBOLComplexPalette = Enum("SBOLComplexPalette",{
    identifiers.external.component_definition_transcriptionFactor : "#a1b4ee"
})
SBOLRolePalette = Enum("SBOLRolePalette",{
    identifiers.external.component_definition_DNA : SBOLDNAPalette,
    identifiers.external.component_definition_DNARegion : SBOLDNAPalette,
    identifiers.external.component_definition_RNA : SBOLRNAPalette,
    identifiers.external.component_definition_RNARegion : SBOLRNAPalette,
    identifiers.external.component_definition_protein : SBOLProteinPalette,
    identifiers.external.component_definition_smallMolecule : SBOLSmallMoleculePalette,
    identifiers.external.component_definition_complex : SBOLComplexPalette
})
SBOLGeneticRolePalette = Enum("SBOLGeneticRolePalette",{
    identifiers.external.component_definition_promoter : "#86E078",
    identifiers.external.component_definition_rbs : "#8C5EE0",
    identifiers.external.component_definition_cds : "#FF675D",
    identifiers.external.component_definition_terminator : "#FAC57D",
    identifiers.external.component_definition_gene : "#5779E0",
    identifiers.external.component_definition_engineeredGene : "#5779E0",
    identifiers.external.component_definition_engineeredRegion : "#E54EF0",
    identifiers.external.component_definition_tag : "#EBD357",
    identifiers.external.component_definition_engineeredTag : "#EBD357",
    identifiers.external.component_definition_operator : "#E07747",
    identifiers.external.component_definition_nonCovBindingSite : "#2f4f4f",
    identifiers.external.component_definition_startCodon : "#F5556F",
    "default" : "#7DF5DF"
})
SBOLClassPalette = Enum("SBOLClassPalette",{
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
SBOLPredicatePalette = Enum("SBOLPredicatePalette",{
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