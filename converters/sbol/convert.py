import networkx as nx
from rdflib import RDF,URIRef
from utility.nv_identifiers import identifiers as nv_ids
from converters.sbol.utility.graph import SBOLGraph

def convert(filename):
    graph = nx.MultiDiGraph()
    sbol_graph = SBOLGraph(filename)
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

    for cd in sbol_graph.get_component_definitions():
        p = RDF.type
        o = nv_ids.objects.entity
        n,node_count = _add_node(cd,node_count)
        v,node_count = _add_node(o,node_count)
        graph.add_edge(n, v, key=p, weight=1)

        for c in sbol_graph.get_components(cd):
            definition = sbol_graph.get_definition(c)
            c,node_count = _add_node(definition,node_count)
            graph.add_edge(n,c,key=nv_ids.predicates.contains,weight=1)
    return graph
