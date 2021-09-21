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
         
    def hierarchy(self):
        edges = []
        node_attrs = {}
        for entity,data in self._builder.get_entities():
            children = self._builder.get_children(entity)
            if len(children) == 0:
                continue
            node_attrs[entity] = data
            for child,key in children:
                child,c_data = child
                node_attrs[child] = c_data
                edge = self._build_edge_attr(key)
                edges.append((entity,child,key,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def interaction_verbose(self):
        edges = []
        node_attrs = {}
        raise NotImplementedError()
        return self._builder.sub_graph(edges,node_attrs)

    def interaction(self):
        edges = []
        node_attrs = {}
        raise NotImplementedError()
        return self._builder.sub_graph(edges,node_attrs)

    def interaction_genetic(self):
        edges = []
        node_attrs = {}
        raise NotImplementedError()
        return self._builder.sub_graph(edges,node_attrs)

    def protein_interaction(self):
        edges = []
        node_attrs = {}
        raise NotImplementedError()
        return self._builder.sub_graph(edges,node_attrs)

    def module(self):
        edges = []
        node_attrs = {}
        raise NotImplementedError()
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