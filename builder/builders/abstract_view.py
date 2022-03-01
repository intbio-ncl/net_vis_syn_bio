import re

class AbstractViewBuilder:
    def __init__(self,builder):
        self._builder = builder

    def full(self):
        return self._builder._graph

    def intersection(self):
        i_graphs = self._builder.get_internal_graphs()
        f_g = i_graphs.pop(0)
        f_g_c = f_g.copy()
        for n_g in i_graphs:
            f_g_c.remove_nodes_from(n for n in f_g if n not in n_g)
            f_g_c.remove_edges_from(e for e in f_g.edges if e not in n_g.edges)
        g = self._builder.sub_graph(new_graph=f_g_c)
        g.remove_isolated_nodes()
        return g

    def difference(self):
        i_graphs = self._builder.get_internal_graphs()
        f_g = i_graphs.pop(0)
        f_g_c = f_g.copy()
        for n_g in i_graphs:
            f_g_c.remove_nodes_from(n for n in f_g if n in n_g)
            f_g_c.remove_edges_from(e for e in f_g.edges if e in n_g.edges)
            
        g = self._builder.sub_graph(new_graph=f_g_c)
        g.remove_isolated_nodes()
        return g

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