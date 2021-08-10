import re

import networkx as nx
from rdflib import RDF,URIRef,OWL
from converters.sbol.utility.graph import SBOLGraph


def convert(filename,model_graph):
    graph = nx.MultiDiGraph()
    sbol_graph = SBOLGraph(filename)
    model_roots = model_graph.get_base_class()
    node_count = 1
    node_map = {}

    def _add_node(entity,node_count):
        if entity in node_map.keys():
            n_key = node_map[entity]
        else:
            n_key = node_count
            node_map[entity] = n_key
            node_count += 1
        if isinstance(entity, URIRef):
            e_type = "URI"
        else:
            e_type = "Literal"
        graph.add_node(n_key, key=entity,type=e_type)
        return n_key,node_count

    nv_role = model_graph.identifiers.predicates.role
    for cd in sbol_graph.get_component_definitions():
        roles = [(nv_role,r) for r in (sbol_graph.get_roles(cd)+sbol_graph.get_types(cd))]
        s,p,o = _map_to_nv(cd,roles,model_roots,model_graph)
        n,node_count = _add_node(s,node_count)
        v,node_count = _add_node(o,node_count)
        name = _get_name(p)
        graph.add_edge(n,v,key=p,display_name=name,weight=1)

        for p,o in _map_entities(cd,sbol_graph,model_graph):
            dp = _get_name(p)
            o,node_count = _add_node(o,node_count)
            graph.add_edge(n,o,key=p,dislay_name=dp,weight=1)
    return graph

def _map_entities(cd,sbol_graph,model_graph):
    triples = []
    part_of = model_graph.identifiers.predicates.partOf
    for sc in [sbol_graph.get_definition(c) for c in sbol_graph.get_components(cd)]:
        triples.append((part_of,sc))
    return triples


def _map_to_nv(identifier,properties,roots,model):
    def model_requirement_depth(nv_class,parent_class=None,depth=0):
        def is_equivalent_class(class_id):
            ecs = model.get_equivalent_classes(class_id)
            if len(ecs) == 0:
                # Classes with no equivalents
                # For us that is just the base class.
                return True
            return _meets_requirements(ecs,parent_class,properties)
        class_id,c_data = nv_class
        if not is_equivalent_class(class_id):
            return (depth,parent_class)
        depth +=1
        # All Requirements met.
        children = model.get_child_classes(class_id)
        cur_lowest_child = (depth,nv_class)
        for child in children:
            ret_val = model_requirement_depth(child,nv_class,depth)
            if ret_val[0] > cur_lowest_child[0]:
                cur_lowest_child = ret_val
        # Get most specialised children or self
        return cur_lowest_child
    for root in roots:
        possible_class = model_requirement_depth(root)
        return (identifier,RDF.type,possible_class[1][1]["key"])

def _meets_requirements(equiv_classes,parent_class,properties):
    def _meets_requirements_inner(equiv_type,requirements,parent_class):
        if equiv_type == OWL.intersectionOf:
            # Equivalent Class with extras.
            # All extras must be met.
            for r in requirements:
                if not _meets_requirements_inner(*r,parent_class):
                    return False
        elif equiv_type == OWL.unionOf:
            # Equiv Class with optional extras.
            for r in requirements:
                if _meets_requirements_inner(*r,parent_class):
                    return True
            else:
                return False
        elif equiv_type == RDF.type:
            # Direct Equivalent Class.
            if requirements[1] == RDF.type and requirements[0]["key"] != parent_class[1]["key"]:
                return False
        else:
            # Single properties (Not Class)
            p_o = (equiv_type,requirements[1]["key"])
            if p_o not in properties:
                return False
        return True

    for equiv_class in equiv_classes:
        # Each Requirement must be met.
        for equiv_type,requirements in equiv_class:
            if not _meets_requirements_inner(equiv_type,requirements,parent_class):
                break
        else:
            return True
    else:
        return False

def _get_name(subject):
    split_subject = _split(subject)
    if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
        return split_subject[-2]
    else:
        return split_subject[-1]

def _split(uri):
    return re.split('#|\/|:', uri)