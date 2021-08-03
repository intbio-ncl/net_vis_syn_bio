import re

from rdflib import RDF,OWL,RDFS
from rdflib import Namespace as RDFNamespace
from rdflib.term import BNode

nv_namespace = RDFNamespace('http://nv_ontology/')

class KnowledgeGraphIdentifiers:
    def __init__(self):
        self.objects = Objects()
        self.predicates = Predicates()
        self.roles = Roles()
    
class Predicates:
    def __init__(self):
        pass

class Objects:
    def __init__(self):
        pass

class Roles:
    def __init__(self):
        pass

def produce_identifiers(graph):
    namespaces = [OWL,RDF.uri,RDFS.uri]
    for n,v,e in graph.search((None,None,None)):
        n,n_data = n
        v,v_data = v
        n_key = n_data["key"]
        v_key = v_data["key"]
        if e == RDF.type and v_key == OWL.Class and not isinstance(n_key, BNode):
            _apply_var_variants(Objects,n_key)
        if v_key == OWL.hasValue:
            _apply_var_variants(Roles,v_key)
        for ns in namespaces:
            if ns in e:
                break
        else:
            _apply_var_variants(Predicates,e)        
    return KnowledgeGraphIdentifiers()

def _apply_var_variants(class_name,key):
    var_name = _get_name(key)
    setattr(class_name, var_name, key)
    lower_var_name = var_name.lower()
    setattr(class_name, lower_var_name, key)
    lower_space_list = []
    for index,l in enumerate(var_name):
        if l.islower():
            lower_space_list.append(l)
        elif index == 0:
            lower_space_list.append(l.lower())
        else:
            lower_space_list.append("_" + l.lower())
    lower_space_name = "".join(lower_space_list)
    setattr(class_name, lower_space_name, key)

def _get_name(subject):
    split_subject = _split(subject)
    if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
        return split_subject[-2]
    else:
        return split_subject[-1]


def _split(uri):
    return re.split('#|\/|:', uri)

