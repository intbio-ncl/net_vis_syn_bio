from rdflib import RDFS,OWL
import re

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

    def requirements(self):
        edges = []
        node_attrs = {}
        for c,c_data in self._builder.get_classes(bnodes=False):
            node_attrs[c] = c_data
            print(c_data["key"])
            e_classes = self._builder.get_equivalent_classes(c)
            for e_class in e_classes:
                for operation in e_class:
                    operation_type = operation[0]
                    data = operation[1]
                    print(operation_type)
                    for d in data:
                        if isinstance(d,tuple):
                            pass
                        if operation_type == OWL.intersectionOf:
                            print(d)
                        elif operation_type == OWL.unionOf:
                            pass
        return self._builder.sub_graph(edges,node_attrs)



def _get_name(subject):
    split_subject = _split(subject)
    if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
        return split_subject[-2]
    elif len(split_subject[-1]) == 3 and _isfloat(split_subject[-1]):
        return split_subject[-2]
    else:
        return split_subject[-1]

def _split(uri):
    return re.split('#|\/|:', uri)

def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False