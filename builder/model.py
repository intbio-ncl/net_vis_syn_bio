from rdflib import RDFS,OWL,RDF,BNode
import networkx as nx

from converters.model import convert
from builder.abstract import AbstractBuilder
from builder.builders.model.view import ViewBuilder
from builder.builders.model.mode import ModeBuilder

class ModelBuilder(AbstractBuilder):
    def __init__(self,graph):
        super().__init__(convert(graph))
        self._view_h = ViewBuilder(self)
        self._mode_h = ModeBuilder(self)


    def set_heirarchy_view(self):
        self.view = self._view_h.heirarchy()
    
    def set_requirements_view(self):
        self.view = self._view_h.requirements()

    def get_classes(self,bnodes=True):
        classes = self._graph.search((None,RDF.type,OWL.Class))
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
        class_id = self._resolve_subject(class_id)
        return [c[1] for c in self._graph.search((class_id,RDFS.subClassOf,None))]

    def get_child_classes(self,class_id):
        class_id = self._resolve_subject(class_id)
        return [c[0] for c in self._graph.search((None,RDFS.subClassOf,class_id))]

    def get_class_depth(self,class_id):
        class_id = self._resolve_subject(class_id)
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
        class_id = self._resolve_subject(class_id)
        requirements = []
        # Each equivalent class (Currently, only one for each class.)
        for n,v,e in self._graph.search((class_id,OWL.equivalentClass,None)):
            requirements.append(self.get_requirements(v[0]))
        return requirements

    def get_requirements(self,class_id):
        requirements = []
        class_props = self._graph.search((class_id,None,None))
        intersections = [c[1] for c in class_props if c[2] == OWL.intersectionOf]
        unions = [c[1] for c in class_props if c[2] == OWL.unionOf]
        for i in intersections:
            requirements.append((OWL.intersectionOf,self.get_intersection(i[0])))
        for u in unions:
            requirements.append((OWL.unionOf, self.get_union(u[0])))
        return requirements    

    def get_intersection(self,identifier):
        return self._get_operator(identifier)

    def get_union(self,identifier):
        res = self._get_operator(identifier)
        return res

    def get_restriction(self,r_id):
        res = self._graph.search((r_id,None,None))
        r_value = [c[1] for c in res if c[2] == OWL.hasValue][0]
        r_property = [c[1] for c in res if c[2] == OWL.onProperty][0]
        return [r_value,r_property[1]["key"]]

    def _get_operator(self,identifier):
        requirements = []
        r = identifier
        while True:
            res = self._graph.search((r,None,None))
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
                requirements.append([[f,f_data],RDF.type])

            if r_data["key"] == RDF.nil:
                break
        return requirements