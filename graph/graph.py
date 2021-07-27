import re
import json
import networkx as nx
from rdflib import URIRef

class NVGraph:
    def __init__(self,graph):
        self._graph = graph
        self._generate_labels()

    def __len__(self):
        return len(self._graph)

    def __eq__(self, obj):
        if not isinstance(obj,self.__class__):
            return False
        return nx.is_isomorphic(self._graph,obj._graph)

    def __iter__(self):
        for n in self._graph.nodes:
            yield n

    @property
    def nodes(self):
        return self._graph.nodes

    @property
    def edges(self):
        return self._graph.edges
    
    @property
    def graph(self):
        return self._graph
    
    @graph.setter
    def graph(self,graph):
        self._graph = graph
    
    def save(self,output):
        g_json = nx.readwrite.json_graph.node_link_data(self._graph)
        with open(output,'w') as f:
            json.dump(g_json,f,indent=2)

    def in_edges(self,node = None,keys = False):
        return self.graph.in_edges(node,keys=keys)
    
    def out_edges(self,node = None,keys = False):
        return self.graph.out_edges(node,keys = keys)

    def search(self,pattern,lazy=False):
        matches = []
        s,p,o = pattern
        if p and not isinstance(p,(list,set,tuple)): 
            p = [p]
        if o and not isinstance(o,(list,set,tuple)):
            o = [o]
        for n,v,k in self.edges(s,keys=True):
            if not p or k in p:
                n_data = self.nodes[n]
                v_data = self.nodes[v]
                if not o or v_data["key"] in o:
                    if lazy:
                        return ([n,n_data],[v,v_data],k)
                    matches.append(([n,n_data],[v,v_data],k))
        return matches

    def add_edge(self,n1,n2,key,**kwargs):
        self._graph.add_edge(n1,n2,key=key,**kwargs)
    
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

    def _generate_labels(self):
        for node,data in self.nodes(data=True):
            if "display_name" not in data.keys():
                identity = data["key"]
                if isinstance(identity,URIRef):
                    name = self._get_name(identity)
                else:
                    name = str(identity)
                self.nodes[node]["display_name"] = name
        for n,v,k,e in self.edges(keys=True,data=True):
            if "display_name" not in e.keys():
                e["display_name"] = self._get_name(k)

def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False



