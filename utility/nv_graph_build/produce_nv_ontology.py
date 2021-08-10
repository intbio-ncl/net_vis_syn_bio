'''
RDFLIB throws many warnings regarding Class & Restriction.
https://github.com/RDFLib/rdflib/issues/1381
I dont think this affects the output.
'''
import warnings
warnings.filterwarnings("ignore")
import sys, inspect

from rdflib import Graph,RDF,OWL
from rdflib.extras import infixowl as owl 

from identifiers import identifiers
from entities import property as nv_property

from entities.entity import *
from entities.physcial_entities import *

def produce_ontology_graph():
    graph = Graph()
    graph.bind('nv', identifiers.namespaces.nv)
    properties = {}
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
        
    for property,domain in properties.items():
        # Unsure how to add the unionOf...
        d = owl.Class(graph=graph)
        owl.Property(property,graph=graph,domain=d)
    graph.serialize("nv_model.xml",format="xml")


def get_properties(obj):
    return ([p.property for p in obj.properties if "property" in dir(p)] + 
           [r.property.property for r in obj.requirements if "property" in dir(r)])

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

def collection_trawl(graph):
    for s,p,o in graph.triples((None,RDF.type,OWL.AllDisjointClasses)):
        for s,p,o in graph.triples((s,OWL.members,None)):
            rest = o
            while rest != RDF.nil:
                triples = list(graph.triples((rest,None,None)))
                rest = [t for t in triples if t[1] == RDF.rest]
                first = [t for t in triples if t[1] == RDF.first]
                if len(rest) != 1 or len(first) != 1:
                    raise ValueError("This Shunna happen bro")
                first = first[0][2]
                rest = rest[0][2]

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