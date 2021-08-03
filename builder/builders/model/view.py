from rdflib import RDFS

from builder.builders.abstract_view import AbstractViewBuilder

class ViewBuilder(AbstractViewBuilder):
    def __init__(self,builder):
        super().__init__(builder)

    def heirarchy(self):
        edges = []
        node_attrs = {}
        def _handle_branch(child):
            for c,c_data in self._builder.get_child_classes(child):
                node_attrs[c] = c_data
                edge = {"display_name" : "SubClassOf"}
                edges.append((child,c,RDFS.subClassOf,edge))
                _handle_branch(c)
        for base,b_data in self._builder.get_base_class():
            node_attrs[base] = b_data
            _handle_branch(base)
        return self._builder.sub_graph(edges,node_attrs)




