import os
import types

from rdflib import RDF

from converters.protocol_handler import convert as p_convert
from converters.model_handler import convert as m_convert

from builder.abstract import AbstractBuilder
from builder.builders.protocol.view import ViewBuilder
from builder.builders.protocol.mode import ModeBuilder


def _add_predicate(obj,predicate):
    method_name = f'get_{predicate.split("/")[-1].lower()}'
    def produce_get_predicate(predicate):
        def produce_get_predicate_inner(self,subject=None,lazy=False):
            return self._graph.search((subject,predicate,None),lazy)
        return produce_get_predicate_inner
    if method_name not in obj.__dict__:
        obj.__dict__[method_name] = types.MethodType(produce_get_predicate(predicate),obj)

def _add_object(obj,subject):
    method_name = f'get_{subject.split("/")[-1].lower()}'
    def produce_get_subject(subject):
        def produce_get_subject_inner(self,lazy=False,children=True):
            if children:
                m_id = self._model_graph.get_class_code(subject)
                subjects = [subject,*[s[1]["key"] for s in self._model_graph.get_derived(m_id)]]
            else:
                subjects = subject
            return self._graph.search((None,RDF.type,subjects),lazy)
        return produce_get_subject_inner
    if method_name not in obj.__dict__:
        obj.__dict__[method_name] = types.MethodType(produce_get_subject(subject),obj)

class ProtocolBuilder(AbstractBuilder):
    def __init__(self,model,graph=None):
        model_graph = m_convert(model)
        super().__init__(p_convert(model_graph,graph))
        self._model_graph = model_graph
        self._view_h = ViewBuilder(self)
        self._mode_h = ModeBuilder(self)
        for predicate in self._model_graph.identifiers.predicates:
            _add_predicate(self,predicate)
        for obj in self._model_graph.identifiers.objects:
            _add_object(self,obj)

    def load(self,fn):
        self._graph = p_convert(self._model_graph,fn)

    def set_action_io_explicit_view(self):
        self.view = self._view_h.io_explicit()

    def set_action_io_aggregate_view(self):
        self.view = self._view_h.io_aggregate()

    def set_action_flow_view(self):
        self.view = self._view_h.flow()

    def set_action_io_implicit_view(self):
        self.view = self._view_h.io_implicit()
    
    def set_heirarchy_view(self):
        self.view = self._view_h.heirarchy()


    # -------------------- Queries --------------------
    def get_actions(self):
        return self._graph.search((None,self._model_graph.identifiers.predicates.actions,None))
        
    def resolve_action(self,action):
        first = None
        rest = None
        actions = []
        while rest != RDF.nil:
            res = self._graph.search((action,None,None))
            first = [c for c in res if c[2] == RDF.first]
            rest = [c for c in res if c[2] == RDF.rest]
            assert(len(first) == 1)
            assert(len(rest) == 1)
            first = first[0][1]
            rest = rest[0][1]
            action = rest[0]
            rest = rest[1]["key"]
            actions.append(first)
        return actions

    def get_io(self,action):
        source_p = self._model_graph.identifiers.predicates.source
        dest_p = self._model_graph.identifiers.predicates.destination
        res = self._graph.search((action,[source_p,dest_p],None))
        sources = [c[1] for c in res if c[2] == source_p]
        dest = [c[1] for c in res if c[2] == dest_p]
        return sources,dest

    def get_parent(self,identifier):
        parent_ps = [self._model_graph.identifiers.predicates.actions,
                    self._model_graph.identifiers.predicates.has_container]
        res = self._graph.search((None,parent_ps,identifier),True)
        if res:
            return res[0]
        return None

    def get_object_code(self,uri):
        for n_id,n_data in self.nodes(data=True):
            if uri == n_data["key"]:
                return n_id
        return None



