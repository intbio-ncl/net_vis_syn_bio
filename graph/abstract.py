import re
import json
import networkx as nx
from rdflib import URIRef,RDF


def _stringify_graph(G):
    ng = nx.MultiDiGraph()
    for n,v,k,d in G.edges(keys=True,data=True):
        n_data = G.nodes[n]
        v_data = G.nodes[v]

        ng.add_node(n,**{key:str(v) for key,v in n_data.items()})
        ng.add_node(v,**{key:str(v) for key,v in v_data.items()})
        ng.add_edge(n,v,str(k),**d)
    return ng

def _adj_list(G,output=None):
    if output is None:
        return "\n".join(nx.generate_adjlist(G))
    else:
        return nx.write_adjlist(G, output)

def _gexf(G,output=None):
    G = _stringify_graph(G)
    if output is None:
        return "\n".join(nx.generate_gexf(G))
    else:
        return nx.write_gexf(G, output)
    
def _gml(G,output=None):
    G = _stringify_graph(G)
    if output is None:
        return "\n".join(nx.generate_gml(G))
    else:
        return nx.write_gml(G, output)

def _graphml(G,output=None):
    G = _stringify_graph(G)
    if output is None:
        return "\n".join(nx.generate_graphml(G))
    else:
        return nx.write_graphml(G, output)

def _cytoscape(G,output=None):
    js = nx.cytoscape_data(G)  
    if output is None:
        return json.dumps(js)
    with open(output, 'w') as outfile:
        json.dump(js, outfile)

save_map = {
"adj-list":_adj_list,
"gexf":_gexf,
"gml":_gml,
"graphml":_graphml,
"cytoscape":_cytoscape,
}

class AbstractGraph:
    def __init__(self,graph=None):
        self._graph = graph

    def __len__(self):
        return len(self._graph)

    def __eq__(self, obj):
        if isinstance(obj,self.__class__):
            return nx.is_isomorphic(self._graph,obj._graph)
        if isinstance(obj,nx.MultiDiGraph):
            return nx.is_isomorphic(self._graph,obj)
        return False

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
    
    def save(self,output=None,d_type="gexf"):
        try:
            return save_map[d_type](self._graph,output)
        except KeyError:
            return

    def generate(self,d_type):
        try:
            print(d_type)
            return save_map[d_type](self._graph)
        except KeyError:
            return

    def get_save_formats(self):
        return list(save_map.keys())
        
    def in_edges(self,node = None,keys = False):
        return self.graph.in_edges(node,keys=keys)
    
    def out_edges(self,node = None,keys = False):
        return self.graph.out_edges(node,keys = keys)

    def search(self,pattern,lazy=False):
        matches = []
        s,p,o = pattern
        if not isinstance(s,(list,set,tuple)):
            s = [s]
        if p and not isinstance(p,(list,set,tuple)): 
            p = [p]
        if o and not isinstance(o,(list,set,tuple)):
            o = [o]
        if s != [None] and not any(x in s for x in self.nodes):
            return []
        for subject in s:
            for n,v,k in self.edges(subject,keys=True):
                if not p or k in p:
                    n_data = self.nodes[n]
                    v_data = self.nodes[v]
                    if not o or v_data["key"] in o or v in o:
                        if lazy:
                            return ([n,n_data],[v,v_data],k)
                        matches.append(([n,n_data],[v,v_data],k))
        return matches

    def add_edge(self,n1,n2,key,**kwargs):
        self._graph.add_edge(n1,n2,key=key,**kwargs)
    
    def remove_node(self,node):
        self._graph.remove_node(node)
    
    def remove_edge(self,n,v,e):
        self._graph.remove_edge(n,v,key=e)
    
    def remove_isolated_nodes(self):
        self._graph.remove_nodes_from(list(nx.isolates(self._graph)))

    def get_rdf_type(self,subject):
        rdf_type = self.search((subject,RDF.type,None),lazy=True)
        if rdf_type != []:
            return rdf_type[1]
    
    def bfs(self,source):
        return nx.bfs_tree(self._graph,source).edges()
    
    def dfs(self,source):
        return nx.dfs_tree(self._graph,source).edges()

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

