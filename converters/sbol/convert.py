import networkx as nx
from rdflib import Graph,RDF,URIRef
from utility.nv_identifiers import identifiers as nv_ids
from converters.sbol.identifiers import identifiers as sbol_ids

def convert(filename):
    graph = nx.MultiDiGraph()
    sbol_graph = Graph()
    sbol_graph.load(filename)
    node_count = 1
    node_map = {}

    def _add_node(entity,node_count):
        if entity in node_map.keys():
            n_key = node_map[entity]
        else:
            n_key = node_count
            node_map[entity] = n_key
            node_count += 1
        
        if isinstance(entity, URIRef):
            e_type = "URI"
        else:
            e_type = "Literal"
        graph.add_node(n_key, key=entity,type=e_type)
        return n_key,node_count

    entities = sbol_graph.triples((None,RDF.type,sbol_ids.objects.component_definition))
    interactions = sbol_graph.triples((None,RDF.type,sbol_ids.objects.interaction))
    for s,p,o in entities:
        o = nv_ids.objects.entity
        n,node_count = _add_node(s,node_count)
        v,node_count = _add_node(o,node_count)
        graph.add_edge(n, v, key=p, weight=1)
        for s,p1,o1 in sbol_graph.triples((s,None,None)):
            if p1 in sbol_ids.predicates.prune:
                continue
            if p1 == RDF.type:
                continue
            v1,node_count = _add_node(o1,node_count)
            graph.add_edge(n, v1, key=p1, weight=1)

    for s,p,o in interactions:
        o = nv_ids.objects.interaction
        n,node_count = _add_node(s,node_count)
        v,node_count = _add_node(o,node_count)
        graph.add_edge(n, v, key=p, weight=1)
        for s,p1,o1 in sbol_graph.triples((s,None,None)):
            if p1 in sbol_ids.predicates.prune:
                continue
            if p1 == RDF.type:
                continue
            v1,node_count = _add_node(o1,node_count)
            graph.add_edge(n, v1, key=p1, weight=1)
    return graph