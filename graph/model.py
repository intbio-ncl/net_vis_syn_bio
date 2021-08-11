from rdflib import RDFS,OWL,RDF,BNode,URIRef

from graph.abstract import AbstractGraph
from utility.identifiers import produce_identifiers

class ModelGraph(AbstractGraph):
    def __init__(self,graph):
        super().__init__(graph)
        self.identifiers = produce_identifiers(self)
        self._generate_labels()
        
    def get_classes(self,bnodes=True):
        classes = self.search((None,RDF.type,OWL.Class))
        f_classes = []
        for s,p,o in classes:
            if isinstance(s[1]["key"],BNode):
                if not bnodes:
                    continue
                f_classes.append(s)
            else:
                f_classes.append(s)
        return f_classes
    
    def get_parent_classes(self,class_id):
        return [c[1] for c in self.search((class_id,RDFS.subClassOf,None))]

    def get_child_classes(self,class_id):
        return [c[0] for c in self.search((None,RDFS.subClassOf,class_id))]

    def get_class_depth(self,class_id):
        def _get_class_depth(c_identifier,depth):
            parent = self.get_parent_classes(c_identifier)
            if parent == []:
                return depth
            depth += 1
            c_identifier = parent[0][0]
            return _get_class_depth(c_identifier,depth)
        return _get_class_depth(class_id,0)
   
    def get_base_class(self):
        bases = []
        for c,data in self.get_classes():
            if isinstance(data["key"], BNode):
                continue
            parents = self.get_parent_classes(c)
            if len(parents) == 0:
                bases.append([c,data])
        return bases

    def get_equivalent_classes(self,class_id):
        requirements = []
        # Each equivalent class (Currently, only one for each class.)
        for n,v,e in self.search((class_id,OWL.equivalentClass,None)):
            requirements.append(self.get_requirements(v[0]))
        return requirements

    def get_requirements(self,class_id):
        requirements = []
        c_triples = self.search((class_id,None,None))
        # IntersectionOf + UnionOf are still classes so 
        # their type triples is added to direct equivalence (Direct propery check.)
        pruned_triples = []
        for n,v,e in c_triples :
            if [c[0] for c in c_triples].count(n) > 1 and e == RDF.type:
                continue
            pruned_triples.append((n,v,e))

        for n,v,e in pruned_triples:
            if e == OWL.intersectionOf:
                requirements.append((OWL.intersectionOf,self.get_intersection(v[0])))
            elif e == OWL.unionOf:
                requirements.append((OWL.unionOf, self.get_union(v[0])))
            elif e == RDF.type:
                #print(n)
                requirements.append((RDF.type,n))
            else:
                requirements.append((e,n))
        
        return requirements    

    def get_intersection(self,identifier):
        return self._get_operator(identifier)

    def get_union(self,identifier):
        res = self._get_operator(identifier)
        return res

    def get_restriction(self,r_id):
        res = self.search((r_id,None,None))
        r_value = [c[1] for c in res if c[2] == OWL.hasValue][0]
        r_property = [c[1] for c in res if c[2] == OWL.onProperty][0]
        return [r_property[1]["key"],r_value]

    def _get_operator(self,identifier):
        requirements = []
        r = identifier
        while True:
            res = self.search((r,None,None))
            f,f_data = [c[1] for c in res if c[2] == RDF.first][0]
            r,r_data = [c[1] for c in res if c[2] == RDF.rest][0]
            if isinstance(f_data["key"], BNode):
                f_type = self.get_rdf_type(f)[1]["key"]
                if f_type == OWL.Restriction:
                    requirements.append(self.get_restriction(f))
                elif f_type == OWL.Class:
                    requirements += self.get_requirements(f)
                else:
                    raise ValueError("Wut")
            elif f in [c[0] for c in self.get_classes(False)]:
                requirements.append((RDF.type,[f,f_data]))
            if r_data["key"] == RDF.nil:
                break
        return requirements

    def _generate_labels(self):
        for node,data in self.nodes(data=True):
            if "display_name" not in data.keys():
                identity = data["key"]
                if isinstance(identity,URIRef):
                    name = (self.identifiers.namespaces.get_code(identity) + 
                            self._get_name(identity))
                else:
                    name = str(identity)
                self.nodes[node]["display_name"] = name
        for n,v,k,e in self.edges(keys=True,data=True):
            if "display_name" not in e.keys():
                e["display_name"] = self._get_name(k)


