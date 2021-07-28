import sys, inspect

from rdflib import Graph

from nv_identifiers import identifiers
from entities.entity import *
from entities.physcial_entities import *

def produce_ontology_graph():
    graph = Graph()

    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if not _is_subclass(obj):
            continue

        obj = obj()
        graph.add((obj.uri,None,None))

def _is_subclass(entity):
    try:
        if not issubclass(entity,Entity):
            return False
    except TypeError:
        return False
    return True

if __name__ == "__main__":
    produce_ontology_graph()