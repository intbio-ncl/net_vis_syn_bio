import os
from rdflib import Graph
import networkx as nx
from graph.model import ModelGraph

def convert(graph):
    if not isinstance(graph,Graph):
        g = Graph()
        g.load(graph)
    else:
        g = graph

    nx_graph = nx.MultiDiGraph()
    node_count = 1
    node_map = {}
    def _add_node(entity,node_count):
        if entity in node_map.keys():
            n_key = node_map[entity]
        else:
            n_key = node_count
            node_map[entity] = n_key
            node_count += 1
        nx_graph.add_node(n_key, key=entity)
        return n_key,node_count

    for s,p,o in g.triples((None,None,None)):
        n,node_count = _add_node(s,node_count)
        v,node_count = _add_node(o,node_count)
        nx_graph.add_edge(n,v,key=p,weight=1)
    return ModelGraph(nx_graph)