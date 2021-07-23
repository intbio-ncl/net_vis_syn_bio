from utility.nv_identifiers import identifiers
import re

class ViewBuilder:
    def __init__(self,builder):
        self._builder = builder

    def full(self):
        return self._builder._graph

    def pruned(self):
        edges = []
        node_attrs = {}
        w_predicates = []
        for n,v,k,e in self._builder.edges(keys=True,data=True):
            if k not in w_predicates:
                continue
            node_attrs[n] = self._builder.nodes[n]
            node_attrs[v] = self._builder.nodes[v]
            edges.append((n,v,k,e))
        return self._builder.sub_graph(edges,node_attrs)
         
    def heirarchy(self):
        edges = []
        node_attrs = {}
        for entity,data in self._builder.get_entities():
            sub_entities = self._builder.get_entities(entity)
            if len(sub_entities) == 0:
                continue
            node_attrs[entity] = data

            for s_entity in sub_entities:
                key = identifiers.predicates.contains
                s_entity,s_e_data = s_entity
                node_attrs[s_entity] = s_e_data
                edge = self._build_edge_attr(key)
                edges.append((entity,s_entity,key,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def interaction_verbose(self):
        edges = []
        node_attrs = {}
        return self._builder.sub_graph(edges,node_attrs)

    def interaction(self):
        edges = []
        node_attrs = {}
        return self._builder.sub_graph(edges,node_attrs)

    def interaction_genetic(self):
        edges = []
        node_attrs = {}
        return self._builder.sub_graph(edges,node_attrs)

    def ppi(self):
        edges = []
        node_attrs = {}
        return self._builder.sub_graph(edges,node_attrs)

    def module(self):
        edges = []
        node_attrs = {}
        return self._builder.sub_graph(edges,node_attrs)
                                              
    def _build_edge_attr(self,key):
        return {"display_name" : self._get_name(key)}

    def _get_name(self,subject):
        split_subject = self._split(subject)
        if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
            return split_subject[-2]
        elif len(split_subject[-1]) == 3 and _isfloat(split_subject[-1]):
            return split_subject[-2]
        else:
            return split_subject[-1]

    def _split(self,uri):
        return re.split('#|\/|:', uri)

def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

