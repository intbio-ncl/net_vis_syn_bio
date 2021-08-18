'''
RDFLIB throws many warnings regarding Class & Restriction.
https://github.com/RDFLib/rdflib/issues/1381
I dont think this affects the output.
'''
import warnings
from rdflib.namespace import RDFS

from rdflib.term import BNode
warnings.filterwarnings("ignore")
import sys, inspect

from rdflib import Graph,RDF,OWL
from rdflib.extras import infixowl as owl 

from identifiers import identifiers

from property import property as nv_property
from entities.entity import *
from entities.physcial_entities import *
from entities.conceptual_entities import *

def produce_ontology_graph():
    graph = Graph()
    graph.bind('nv', identifiers.namespaces.nv)
    properties = {}
    requirements = {}

    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if not _is_entity(obj):
            continue
        obj = obj()
        parents = _get_parents(obj)        
        equivalents = _get_equivalence(obj,graph)
        if obj.disjoint:
            disjointed = _get_disjoint_siblings(obj)
        else:
            disjointed = []

        owl.Class(obj.uri,graph=graph,disjointWith=disjointed,
              subClassOf=parents,equivalentClass=equivalents)
        
        for p in get_properties(obj):
            if p in properties.keys():
                properties[p].append(obj.uri)
            else:
                properties[p] = [obj.uri]

        for r in get_requirements(obj):
            if r in requirements.keys():
                requirements[r].append(obj.uri)
            else:
                requirements[r] = [obj.uri]

    for requirement,domain in requirements.items():
        owl.Property(requirement,graph=graph)

    for property,domain in properties.items():
        # Never figured out how to add unions to Class so did it manually.
        range = property.range.uri()
        property = property.property

        domain_node = BNode()
        graph.add((property,RDF.type,OWL.ObjectProperty))
        graph.add((property,RDFS.range,range))
        graph.add((property,RDFS.domain,domain_node))

        union_node = BNode()
        graph.add((domain_node,RDF.type,OWL.Class))
        graph.add((domain_node,OWL.unionOf,union_node))
        cur_node = union_node

        reduced_domain = []
        # Use the most base classes only.
        for index,d in enumerate(domain):
            if not any(x in 
                [t[2] for t in graph.triples((d,RDFS.subClassOf,None))] for x in domain):
                reduced_domain.append(d)

        for index,d in enumerate(reduced_domain):
            if index == len(reduced_domain) - 1:
                next_node = RDF.nil
            else:
                next_node = BNode()
            graph.add((cur_node,RDF.first,d))
            graph.add((cur_node,RDF.rest,next_node))
            cur_node = next_node
        
    graph.serialize("nv_model.xml",format="xml")

def get_requirements(obj):
    return [r.property.property for r in obj.requirements if "property" in dir(r)]

def get_properties(obj):
    return [p for p in obj.properties if "property" in dir(p)]

def _get_parents(obj):
    parents = obj.__class__.__bases__
    return [p().uri for p in parents if p != object]

def _get_disjoint_siblings(obj):
    siblings = []
    parents = obj.__class__.__bases__
    for p in parents:
        children = p.__subclasses__()
        siblings += [c().uri for c in children if c.__name__ != obj.__class__.__name__]
    return siblings

def _get_equivalence(obj,graph):
    equivalents = []
    for parent in obj.__class__.__bases__:
        if parent == object:
            continue
        equivalent = owl.Class(parent().uri,graph=graph)
        for r in obj.requirements:
            sub_equiv = None
            property = r.property
            for index,value in enumerate(r.values):
                if index == 0:
                    sub_equiv = owl.Restriction(property.property,value=value,graph=graph)
                else:
                    sub_equiv = sub_equiv | owl.Restriction(property.property,value=value,graph=graph)
            equivalent = equivalent & sub_equiv
        equivalents.append(equivalent)
    return equivalents

def _is_entity(entity):
    try:
        if not issubclass(entity,Entity):
            return False
    except TypeError:
        return False
    return True


def _is_property(prop):
    try:
        if not issubclass(prop,nv_property.Property):
            return False
    except TypeError:
        return False
    return True

if __name__ == "__main__":
    produce_ontology_graph()