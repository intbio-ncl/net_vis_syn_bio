from rdflib import URIRef
import networkx as nx

from graphs.abstract_graph import AbstractGraph
from util.sbol_identifiers import identifiers

class SBOLGraph(AbstractGraph):
    def __init__(self,graph):
        super().__init__(graph)       

    def get_component_definitions(self):
        return [cd[0] for cd in self.search((None,identifiers.predicates.rdf_type,
                                identifiers.objects.component_definition))]

    def get_component_instances(self):
        return self.search((None,[identifiers.predicates.component,
                identifiers.predicates.functional_component],None))

    def get_module_definitions(self):
        return [md[0] for md in self.search((None,identifiers.predicates.rdf_type,
                                            identifiers.objects.module_definition))]


    def get_definition(self,component):
        definition = self.search((component,identifiers.predicates.definition,None),lazy=True)
        if definition != []:
            return definition[1]

    def get_type(self,subject):
        r_type = self.search((subject,identifiers.predicates.type,None),lazy=True)
        if r_type != []:
            return r_type[1]

    def get_role(self,subject):
        role = self.search((subject,identifiers.predicates.role,None),lazy=True)
        if role != []:
            return role[1]

    def get_types(self,subject):
        return [t[1] for t in self.search((subject,identifiers.predicates.type,None))]
        
    def get_roles(self,subject):
        return [t[1] for t in self.search((subject,identifiers.predicates.role,None))]

    def get_participations(self,interaction):
        return [i[1] for i in self.search((interaction,identifiers.predicates.participation,None))] 

    def get_sequence_annotations(self,cd):
        return [sa[1] for sa in self.search((cd,identifiers.predicates.sequence_annotation,None))]

    def get_sequence_constraints(self,cd):
        return [sc[1] for sc in self.search((cd,identifiers.predicates.sequence_constraint,None))]

    def get_locations(self,sa):
        return [l[1] for l in self.search((sa,identifiers.predicates.location,None))]

    def get_components(self,cd=None,sa=None):
        if cd is not None: s = cd
        elif sa is not None: s = sa
        else: s = None
        return [c[1] for c in self.search((s,identifiers.predicates.component,None))]
    
    def get_modules(self,md=None):
        if md is not None: s = md
        return [c[1] for c in self.search((s,identifiers.predicates.module,None))]

    def get_interactions(self,md=None):
        return [i[1] for i in self.search((md,identifiers.predicates.interaction,None))]

    def get_functional_components(self,md=None):
        return [fc[1] for fc in self.search((md,identifiers.predicates.functional_component,None))]

    def get_component_definition(self,participation=None):
        if participation is not None:
            fc = self.search((participation,identifiers.predicates.participant,None),lazy=True)
            if fc is None:
                return None
            fc = fc[1][1]["key"]
            cd = self.get_definition(fc)
            return cd

    def get_heirachy_instances(self,cd=None):
        return [c[0] for c in self.search((None,identifiers.predicates.definition,cd))]

    def get_top_levels(self):
        return [tl[0] for tl in self.search((None,identifiers.predicates.rdf_type,identifiers.objects.top_levels))]

    def get_maps_to(self,md=None):
        return [m[1] for m in self.search((md,identifiers.predicates.maps_to,None))]
    
    def get_property(self,subject,predicate):
        return [p[1] for p in self.search((subject,predicate,None))]