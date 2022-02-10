from rdflib import RDFS,OWL,RDF
import re

from builder.builders.abstract_view import AbstractViewBuilder

class ViewBuilder(AbstractViewBuilder):
    def __init__(self,builder):
        super().__init__(builder)

    def hierarchy(self):
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
        node_index = self._builder.get_next_index() + 1
        
        def _requirements_inner(subject,equiv_type,requirements):
            nonlocal node_index
            if equiv_type == OWL.intersectionOf:
                node_index += 1
                and_node = node_index
                node_attrs[and_node] = _node_label(OWL.intersectionOf)
                for r in requirements:
                    _requirements_inner(and_node,*r)
                edge = _edge_label("product")
                edges.append((and_node,subject,OWL.intersectionOf,edge))

            elif equiv_type == OWL.unionOf:
                node_index += 1
                or_node = node_index 
                node_attrs[or_node] = _node_label(OWL.unionOf)
                for r in requirements:
                    _requirements_inner(or_node,*r)
                edge = _edge_label("product")
                edges.append((or_node,subject,OWL.unionOf,edge))

            elif equiv_type == RDF.type:
                node_attrs[requirements[0]] = requirements[1]
                edge = _edge_label("isClass")
                edges.append((requirements[0],subject,RDFS.subClassOf,edge))

            else:
                node_attrs[requirements[0][0]] = requirements[0][1]
                edge = _edge_label("hasRole")
                edges.append((requirements[0][0],subject,self._builder.identifiers.predicates.role,edge))

        for c,c_data in self._builder.get_classes(bnodes=False):
            node_attrs[c] = c_data
            e_classes = self._builder.get_equivalent_classes(c)
            for e_class in e_classes:
                for equiv_type,requirements in e_class:
                    _requirements_inner(c,equiv_type,requirements)
        return self._builder.sub_graph(edges,node_attrs)

    def relation(self):
        node_attrs = {}
        edges = []
        def _handle_union(r):
            for r,r_data in self._builder.get_union(r):
                for r in self._builder.resolve_union(r):
                    yield r[1]

        # For each union in each range/domain combo add and edge.
        for p,data in self._builder.get_properties():
            range_data = self._builder.get_range(p)
            if len(range_data) == 0:
                continue
            r,r_data = range_data
            for r,r_data in _handle_union(r):
                d,d_data = self._builder.get_domain(p)
                for e,e_data in _handle_union(d):
                    node_attrs[r] = r_data
                    node_attrs[e] = e_data
                    edge = _edge_label(_get_name(data["key"]))
                    edges.append((r,e,data["key"],edge))
        return self._builder.sub_graph(edges,node_attrs)


def _node_label(key):
    return {"key" : key, "display_name" : _get_name(key)}

def _edge_label(name):
    return {"display_name" : name}

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