'''
RDFLIB throws many warnings regarding Class & Restriction.
https://github.com/RDFLib/rdflib/issues/1381
I dont think this affects the output.
'''
import warnings
warnings.filterwarnings("ignore")
import sys, inspect

from rdflib.namespace import RDFS
from rdflib.term import BNode
from rdflib import Graph,RDF,OWL
from rdflib.extras import infixowl as owl 

from identifiers import identifiers
from datatype.datatype import Input, Output
from entities.abstract_entity import Entity
from datatype.datatype import Datatype
from property import property as nv_property

def produce_ontology(context):
    graph = Graph()
    graph.bind('nv', identifiers.namespaces.nv)
    properties = {}
    requirements = {}
    datatypes = []

    for name, obj in inspect.getmembers(sys.modules[context]):
        if not is_entity(obj): continue
        obj = obj()
        parents = get_parents(obj)        
        equivalents = get_equivalence(obj,graph)
        if obj.disjoint:
            disjointed = get_disjoint_siblings(obj)
        else:
            disjointed = []
        
        restrictions = []
        for r in obj.restrictions:
            annotation_n = BNode()
            prop = r.property
            recipe = r.recipe.recipe
            # Just add it to the graph as annotations.
            list_node = BNode()
            graph.add((annotation_n,OWL.members,list_node))
            cur_node = list_node
            for index,d in enumerate(recipe):
                if index == 0:
                    properties = get_inputs(obj,properties,d,obj)
                if index == len(recipe) - 1:
                    next_node = RDF.nil
                    properties = get_outputs(obj,properties,d,obj)
                else:
                    next_node = BNode()
                graph.add((cur_node,RDF.first,d.uri))
                graph.add((cur_node,RDF.rest,next_node))
                cur_node = next_node
            restrictions.append(owl.Restriction(prop.property,
                                value=annotation_n,graph=graph))

            # No data on the restriction node.
            if prop in properties.keys():
                properties[prop].append(obj.uri)
            else:
                properties[prop] = [obj.uri]

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

        owl.Class(obj.uri,graph=graph,disjointWith=disjointed,
              subClassOf=parents+restrictions,equivalentClass=equivalents)
    graph,datatypes = add_properties(properties,graph,datatypes)
    graph = add_requirements(requirements,graph)
    for datatype in datatypes:
        graph.add((datatype.uri,RDF.type,RDFS.Datatype))
    return graph

def add_properties(properties,graph,datatypes):
    for property,domain in properties.items():
        # Never figured out how to add unions to Class so did it manually.
        prop = property.property
        domain_node = BNode()
        graph.add((prop,RDF.type,OWL.ObjectProperty))
        graph.add((prop,RDFS.domain,domain_node))
        reduced_domain = []
        for d in domain:
            parents = [c[2] for c in graph.triples((d,RDFS.subClassOf,None))]
            if len(list(set(parents) - set(domain))) == 0:
                continue
            reduced_domain.append(d)
        graph = add_union(graph, domain_node, reduced_domain)
        p_range = property.range
        if p_range != [None]:
            range_node = BNode()
            graph.add((prop,RDFS.range,range_node))
            p_range = [p.uri() for p in p_range]
            graph = add_union(graph, range_node, p_range)
        for p in property.properties:
            if p.default_value is not None:
                default_v_uri = p.default_value.uri
                graph.add((prop,p.property,default_v_uri))
                if isinstance(p.default_value, Datatype):
                    datatypes.append(p.default_value)
        for equivalents in property.equivalents:
            for equivalent in equivalents.equivalents:
                graph.add((prop,OWL.equivalentProperty,equivalent))
    return graph,datatypes

def add_requirements(requirements,graph):
    for requirement,domain in requirements.items():
        owl.Property(requirement,graph=graph)
    return graph
    
def get_requirements(obj):
    for e in obj.equivalents:
        for r in e.restrictions:
            if "property" in dir(r):
                yield r.property.property


def get_properties(obj):
    return [p for p in obj.properties if "property" in dir(p)]


def get_inputs(obj, properties, recipe, entity):
    return get_io(obj, properties, recipe, entity, Input)


def get_outputs(obj, properties, recipe, entity):
    return get_io(obj, properties, recipe, entity, Output)


def get_io(o, p, r, e, t):
    # Check if object has a i/o property set already.
    for prop in o.properties:
        for pp in prop.properties:
            if isinstance(pp.default_value, t):
                return p

    for i in [e for e in r.properties for x in e.properties if isinstance(x.default_value, t)]:
        if i in p.keys():
            p[i].append(e.uri)
        else:
            p[i] = [e.uri]
    return p


def get_inheritence(identifier, graph):
    parents = []

    def get_class_depth(c_identifier):
        nonlocal parents
        parent = [t[2] for t in graph.triples((c_identifier, RDFS.subClassOf, None))
                  if not isinstance(t[2], BNode)]
        if parent == []:
            return parents
        parents += parent
        for p in parent:
            return get_class_depth(p)
    return get_class_depth(identifier)


def add_union(graph, subject, union):
    union_node = BNode()
    graph.add((subject, RDF.type, OWL.Class))
    graph.add((subject, OWL.unionOf, union_node))
    cur_node = union_node
    for index, d in enumerate(union):
        if index == len(union) - 1:
            next_node = RDF.nil
        else:
            next_node = BNode()
        graph.add((cur_node, RDF.first, d))
        graph.add((cur_node, RDF.rest, next_node))
        cur_node = next_node
    return graph


def get_parents(obj):
    parents = obj.__class__.__bases__
    return [p().uri for p in parents if p != object]


def get_disjoint_siblings(obj):
    siblings = []
    parents = obj.__class__.__bases__
    for p in parents:
        children = p.__subclasses__()
        siblings += [c().uri for c in children if c.__name__ !=
                     obj.__class__.__name__]
    return siblings


def get_equivalence(obj, graph):
    equivalents = []
    for parent in obj.__class__.__bases__:
        if parent == object:
            continue
        equivalent = owl.Class(parent().uri, graph=graph)
        for e in obj.equivalents:
            for r in e.restrictions:
                sub_equiv = None
                property = r.property
                for index, value in enumerate(r.values):
                    if index == 0:
                        sub_equiv = owl.Restriction(
                            property.property, value=value, graph=graph)
                    else:
                        sub_equiv = sub_equiv | owl.Restriction(
                            property.property, value=value, graph=graph)
                equivalent = equivalent & sub_equiv
        equivalents.append(equivalent)
    return equivalents


def is_entity(entity):
    try:
        if not issubclass(entity, Entity):
            return False
    except TypeError:
        return False
    return True


def is_property(prop):
    try:
        if not issubclass(prop, nv_property.Property):
            return False
    except TypeError:
        return False
    return True
