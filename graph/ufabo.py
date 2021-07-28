from os import path
from owlready2 import *
from functools import partial
ufab_fn = path.join(path.dirname(path.realpath(__file__)),"ufabo.rdf")

class UFABGraph:
    def __init__(self):
        self._graph = get_ontology(ufab_fn)
        self._graph.load()

    def __getattr__(self, name):
        class_name = name.split("_")[-1].lower()
        for o_class in self._graph.classes():
            print(o_class.name,class_name)
            if o_class.name.lower() == class_name:
                return partial(self._graph.search,is_a=o_class)
        raise ValueError(f'No method named {name}.')

    def search(self,pattern,lazy=False):
        if lazy:
            for res in self.graph.triples(pattern):
                return res
            return None
        else:
            results = []
            for res in self.graph.triples(pattern):
                results.append(res)
            return results
    
    def get_equivalent(self,object):
        return list(default_world.sparql("""SELECT (?x AS ?nb){ ?x a owl:Class . }"""))


    def dump(self):
        return list(default_world.sparql("""SELECT ?s ?p ?o
                                    WHERE{ ?s ?p ?o }
                                """))

    def get_entity_type(self,role):
        '''
        Given a external Ontology URI, return corresponding ontology class
        '''
        for e in self._graph.properties():
            print(e)
        for entity in self.get_PhysicalEntity():
            res = self._graph.search(equivalent_class=entity)
            print(len(list(res)))
            for e in res:
                pass#print(e)

        return None
        r_v= self._graph.search(iri=role)
        for r in r_v:
            print(dir(r))
            for res in self._graph.search(r):
                print("Res")
                print(res)
