import re
import networkx as nx
from networkx.algorithms.centrality import degree_centrality
from rdflib import URIRef,Graph,RDF

class AbstractGraph:
    def __init__(self,graph):
        if isinstance(graph,nx.MultiDiGraph):
            self._graph = graph
            if len(self._graph) > 0:
                self._max_key = max([node for node in self._graph.nodes])
            else:
                self._max_key = 1
        else:
            _graph = Graph()
            _graph.load(graph)
            self._graph,self._max_key = _rdf_to_networkx(_graph)
        self._generate_labels()

    def __len__(self):
        return len(self._graph)

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

    @property
    def max_key(self):
        self._max_key += 1
        return self._max_key
    
    @max_key.setter
    def max_key(self,increase):
        self._max_key += increase
        
    def degree_centrality(self):
        return degree_centrality(self._graph)
    
    def in_edges(self,node = None,keys = False):
        return self.graph.in_edges(node,keys=keys)
    
    def out_edges(self,node = None,keys = False):
        return self.graph.out_edges(node,keys = keys)

    def merge_nodes(self,node1,node2):
        node1_data = self.nodes[node1]["key"]
        for n,v,k,e in self._graph.in_edges(node2,data=True,keys=True):
            new_key = (k[0],k[1],node1_data)
            self.add_edge(n,node1,new_key,**e)
        for n,v,k,e in self._graph.out_edges(node2,data=True,keys=True):
            new_key = (node1_data,k[1],k[2])
            self.add_edge(node1,v,new_key,**e)

        self.remove_node(node2)

    def remove_edge(self,n1,n2):
        self._graph.remove_edge(n1,n2)
    
    def remove_node(self,n1):
        self._graph.remove_node(n1)

    def remove_isolated_nodes(self):
        self._graph.remove_nodes_from(list(nx.isolates(self._graph)))
        
    def is_connected(self):
        return nx.is_connected(self._graph)

    def search(self,pattern,lazy=False):
        matches = []
        s,p,o = pattern
        if s: s = self.get_entity_code(s)
        if p and not isinstance(p,(list,set,tuple)): 
            p = [p]
        if o and not isinstance(o,(list,set,tuple)):
            o = [o]
        for n,v,e in self.edges(s,keys=True):
            if not p or e[1] in p:
                n_data = self.nodes[n]
                v_data = self.nodes[v]
                if not o or v_data["key"] in o:
                    if lazy:
                        return ([n,n_data],[v,v_data],e)
                    matches.append(([n,n_data],[v,v_data],e))
        return matches


    def get_entity_code(self,entity):
        for node,data in self.nodes(data=True):
            if data["key"] == entity or node == entity:
                return node
        import pdb;pdb.set_trace()
        raise ValueError(f"Can't find code for {entity}")
        
    def add(self,edges):
        self._graph.add_edges_from(edges)
    
    def add_edge(self,n1,n2,key,**kwargs):
        self._graph.add_edge(n1,n2,key=key,**kwargs)
    
    def set_node_attr(self,node_id,node_data):
        for k,v in node_data.items():
            self._graph.nodes[node_id][k] = v

    def get_tree(self):
        tree_edges = []
        node_attrs = {}
        seen = []
        for n,v,e in self._graph.edges:
            node_attrs[v] = self.nodes[v]
            node_attrs[n] = self.nodes[n]
            v_copy = v
            if v in seen:
                v = self.max_key
                node_attrs[v] = self.nodes[v_copy]
                seen.append(v)
            else:
                seen.append(v)
            edge = self._create_edge_dict(e)
            tree_edges.append((n,v,e,edge))       
        tree_graph = self.sub_graph(tree_edges,node_attrs)
        return tree_graph

    def get_network(self):
        return self
        
    def sub_graph(self,edges,node_attrs = {}):
        new_graph = nx.MultiDiGraph()
        new_graph.add_edges_from(edges)
        for subject,node,edge in new_graph.edges:
            try:
                new_graph.nodes[subject].update(node_attrs[subject])
            except (KeyError,ValueError):
                pass
            try:
                new_graph.nodes[node].update(node_attrs[node])
            except (KeyError,ValueError):
                pass
        new_graph = self.__class__(new_graph)
        return new_graph

    def get_rdf_type(self,subject):
        rdf_type = self.search((subject,RDF.type,None),lazy=True)
        if rdf_type != []:
            return rdf_type[1]

    def _create_edge_dict(self,key,weight=1):
        edge = {'weight': weight, 
                'display_name': self._get_name(str(key[1]))}
        return edge

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

        for subject,node,edge in self.edges:
            edge_data = self.edges[subject,node,edge]
            if "display_name" not in edge_data.keys():
                nx.set_edge_attributes(self._graph,{(subject,node,edge) : {"display_name" : self._get_name(edge[1])}})

def _rdf_to_networkx(graph):
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
    for s,p,o in graph:
        n,node_count = _add_node(s,node_count)
        v,node_count = _add_node(o,node_count)
        nx_graph.add_edge(n, v, key=(s,p,o), weight=1)
    return nx_graph, node_count + 1


def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False



