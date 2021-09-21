from rdflib import RDFS,OWL,RDF,BNode,URIRef

from graph.abstract import AbstractGraph
from utility.identifiers import produce_identifiers

class ModelGraph(AbstractGraph):
    def __init__(self,graph):
        super().__init__(graph)
        self.identifiers = produce_identifiers(self)
        self._generate_labels()
        
    def get_class_code(self,label):
        for n,data in self.nodes(data=True):
            if label == data["key"]:
                return n
        raise ValueError(f'{label} is not in graph.')

    def get_child_predicate(self):
        return self.identifiers.predicates.partOf

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
    
    def is_base(self,parent,child):
        def up_search(p,c):
            for cp in self.get_parent_classes(c):
                if cp[0] == parent:
                    return True
                if up_search(cp[0],p):
                    return True
            return False
        return up_search(parent,child)

    def is_derived(self,child,parent):
        def down_search(c,p):
            for cc in self.get_child_classes(p):
                if cc[1]["key"] == child:
                    return True
                if down_search(c,cc[0]):
                    return True
            return False
        return down_search(child,parent)

    def get_parent_classes(self,class_id):
        return [c[1] for c in self.search((class_id,RDFS.subClassOf,None)) 
                if not isinstance(c[1][1]["key"],BNode)]

    def get_child_classes(self,class_id):
        return [c[0] for c in self.search((None,RDFS.subClassOf,class_id)) 
                if not isinstance(c[1][1]["key"],BNode)]
    
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

    def get_class_properties(self,class_id):
        properties = []
        def up_search(identifier):
            for q,w,e in self.search((None,None,identifier)):
                if e == RDFS.domain:
                    properties.append(q)
                elif e == RDF.rest or e == OWL.unionOf:                    
                    up_search(q[0])
        for n,v,k in self.search((None,RDF.first,class_id)):
            up_search(n[0])
        return properties

    def get_restrictions_on(self,class_id):
        restrictions = []
        for p,p_data in [c[1] for c in self.search((class_id,RDFS.subClassOf,None)) if isinstance(c[1][1]["key"],BNode)]:
            rdf_type = self.get_rdf_type(p)[1]["key"]
            if rdf_type == OWL.Restriction:
                restrictions.append(p)
        return restrictions

    def get_constraint(self,restriction_id):
        constraints = [OWL.allValuesFrom,
                       OWL.someValuesFrom,
                       OWL.hasValue]
        p = None
        c_p = None
        c_v = None
        for n,v,k in self.search((restriction_id,None,None)):
            if k == OWL.onProperty:
                p = v[1]["key"]
            elif k in constraints:
                c_p = k
                c_v = v[0]
        if p is None or c_p is None or c_v is None:
            raise ValueError(f'{restriction_id} is malformed, no constraint.')
        for n,v,k in self.search((c_v,OWL.members,None)):
            constraint = self._get_operator(v[0])
        return p,constraint

    def get_properties(self):
        return [p[0] for p in self.search((None,RDF.type,OWL.ObjectProperty))]

    def get_domain(self,subject):
        r = self.search((subject,RDFS.domain,None),True)
        if r is not None and r != []:
            r = r[1]
        return r

    def get_range(self,subject):
        r = self.search((subject,RDFS.range,None),True)
        if r is not None and r != []:
            r = r[1]
        return r

    def get_union(self,subject):
        return [r[1] for r in self.search((subject,OWL.unionOf,None))]

    def get_equivalent_classes(self,class_id):
        requirements = []
        # Each equivalent class (Currently, only one for each class.)
        for n,v,e in self.search((class_id,OWL.equivalentClass,None)):
            requirements.append(self.get_requirements(v[0]))
        return requirements

    def get_equivalent_properties(self,property_id):
        return [e[1] for e in self.search((property_id,OWL.equivalentProperty,None))]

    def get_requirements(self,class_id):
        requirements = []
        class_data = self.nodes[class_id]
        if not isinstance(class_data["key"],BNode):
            return [(RDF.type,[class_id,class_data])]
        c_triples = self.search((class_id,None,None))
        # IntersectionOf + UnionOf are still classes so 
        # their type triples is added to direct equivalence (Direct propery check.)
        pruned_triples = []
        for n,v,e in c_triples :
            if [c[0] for c in c_triples].count(n) > 1 and e == RDF.type:
                continue
            if e == RDFS.subClassOf or e == OWL.equivalentClass:
                continue
            pruned_triples.append((n,v,e))

        for n,v,e in pruned_triples:
            if e == OWL.intersectionOf:
                requirements.append((OWL.intersectionOf,self.resolve_intersection(v[0])))
            elif e == OWL.unionOf:
                requirements.append((OWL.unionOf, self.resolve_union(v[0])))
            elif e == RDF.type:
                requirements.append((RDF.type,n))
            else:
                requirements.append((e,n))
        return requirements    

    def resolve_intersection(self,identifier):
        return self._get_operator(identifier)

    def resolve_union(self,identifier):
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
            f = [c[1] for c in res if c[2] == RDF.first]
            r = [c[1] for c in res if c[2] == RDF.rest]
            if f == [] or r == []:
                return requirements
            f,f_data = f[0]
            r,r_data = r[0]
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


