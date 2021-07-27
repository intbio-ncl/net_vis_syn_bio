import re 

class ModeBuilder:
    def __init__(self,builder):
        self._builder = builder

    def tree(self):
        tree_edges = []
        node_attrs = {}
        seen = []
        max_key = max([node for node in self._builder.v_nodes])
        for n,v,e in self._builder.v_edges:
            node_attrs[v] = self._builder.nodes[v]
            node_attrs[n] = self._builder.nodes[n]
            v_copy = v
            if v in seen:
                max_key +=1
                v = max_key
                node_attrs[v] = self._builder.nodes[v_copy]
                seen.append(v)
            else:
                seen.append(v)
            edge = self._create_edge_dict(e)
            tree_edges.append((n,v,e,edge))       
        tree_graph = self._builder.sub_graph(tree_edges,node_attrs)
        return tree_graph

    def network(self):
        return self._builder.view

    def _create_edge_dict(self,key,weight=1):
        edge = {'weight': weight, 
                'display_name': self._get_name(str(key))}
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

def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False