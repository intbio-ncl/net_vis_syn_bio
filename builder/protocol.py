import types

from rdflib import RDF,URIRef
from rdflib.term import BNode

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
    
    def set_hierarchy_view(self):
        self.view = self._view_h.hierarchy()

    def set_pruned_view(self):
        self.view = self._view_h.pruned()

    def set_instructions_view(self,level,detail):
        self.view = self._view_h.instructions(level,detail)

    def set_flow_view(self,level,detail):
        self.view = self._view_h.flow(level,detail)

    def set_io_view(self,level,detail):
        self.view = self._view_h.io(level,detail)

    def set_process_view(self,level,detail):
        self.view = self._view_h.process(level,detail)

    def set_container_view(self,detail):
        self.view = self._view_h.container(detail)

    # -------------------- Queries --------------------
    def get_actions(self):
        return self._graph.search((None,self._model_graph.identifiers.predicates.actions,None))

    def get_proto_actions(self):
        protocol_p = self._model_graph.identifiers.objects.protocol
        action_p = self._model_graph.identifiers.objects.action
        protocol_p_code = self._model_graph.get_class_code(protocol_p)
        action_p_code = self._model_graph.get_class_code(action_p)
        objs = ([protocol_p,action_p] + 
                [p[1]["key"] for p in self._model_graph.get_child_classes(protocol_p_code)] + 
                [p[1]["key"] for p in self._model_graph.get_child_classes(action_p_code)])
        return self._graph.search((None,RDF.type,objs))
    
    def get_action_node(self,subject):
        res = self._graph.search((subject,self._model_graph.identifiers.predicates.actions,None),True)
        if res == []:
            return None
        return res[1]
    
    def get_well_actions(self,well_id):
        nv_wells = [self._model_graph.identifiers.predicates.source,
                    self._model_graph.identifiers.predicates.destination,
                    self._model_graph.identifiers.predicates.object]
        return self._graph.search((None,nv_wells,well_id))

    def get_io(self,subject,use_objects=True):
        nv_source = self._model_graph.identifiers.predicates.source
        nv_dest = self._model_graph.identifiers.predicates.destination
        nv_object = self._model_graph.identifiers.predicates.object
        nv_container = self._model_graph.identifiers.objects.container
        preds = [nv_source,nv_object,nv_dest]

        def _run(subj):
            results = self._graph.search((subj,preds,None))
            if use_objects:
                inputs = [r[1] for r in results if r[2] == nv_source or r[2] == nv_object]
                outputs =[r[1] for r in results if r[2] == nv_dest or r[2] == nv_object]
            else:
                inputs = [r[1] for r in results if r[2] == nv_source]
                outputs =[r[1] for r in results if r[2] == nv_dest]
            if inputs == [] and outputs == []:
                assert(inputs ==[] and outputs == [])
                a_node = self.get_action_node(subj)
                if a_node is not None:
                    for action in self.resolve_action(a_node[0]):
                        i,o = _run(action[0])
                        inputs += i
                        outputs += o
            return inputs,outputs
        inputs,outputs = _run(subject)

        def _resolve(items):
            new_items = []
            seens = []
            for i_id,i_data in items:
                i_type = self.get_rdf_type(i_id)
                assert(i_type is not None)
                if i_id in seens:
                    continue
                seens.append(i_id)
                if self._model_graph.is_derived(i_type[1]["key"],nv_container):
                    for _,v,_ in self.get_children(i_id):
                        new_items.append(v)
                else:
                    new_items.append((i_id,i_data))
            return new_items
            
        return _resolve(inputs),_resolve(outputs)

    def get_properties(self,subject):
        props = []
        for n,v,e in self._graph.search((subject,None,None)):
            if isinstance(v[1]["key"],BNode):
                continue
            if e == RDF.type:
                continue
            props.append((n,v,e))
        return props
    
    def get_containers(self,subject):
        return self._graph.search((subject,self._model_graph.identifiers.predicates.has_container,None))

    def get_root(self):
        m_obj = self._model_graph.identifiers.objects.master_protocol
        res = self._graph.search((None,RDF.type,m_obj),True)
        if res == []:
            return None
        return res[0]

    def get_wells(self,subject,use_children=False):
        nv_container = self._model_graph.identifiers.predicates.has_container
        nv_well = self._model_graph.identifiers.predicates.well
        nv_actions = self._model_graph.identifiers.predicates.actions
        nv_object = self._model_graph.identifiers.predicates.object

        nv_wells = [self._model_graph.identifiers.predicates.source,
                    self._model_graph.identifiers.predicates.destination,
                    nv_object,
                    nv_well]
        wells = []
        seens = []
        def _get_wells(subj):
            nonlocal wells
            containers = [subj] + [n[1][0] for n in self.get_containers(subj)]
            if use_children:
                for n,v,e in self.get_children(subj):
                    if e == nv_container:
                        containers.append(v[0])
                    elif e == nv_actions:
                        for action,action_data in self.resolve_action(v[0]):
                            _get_wells(action)
                    elif e == nv_well and v[0] not in seens:
                        wells.append(v)
                        seens.append(v[0])
            for n,v,e in self._graph.search((containers,nv_wells,None)):
                if e == nv_object:
                     _get_wells(v[0])
                     continue
                if v[0] not in seens:
                    wells.append(v)
                    seens.append(v[0])
        _get_wells(subject)
        return wells

    def get_abstraction_level(self,level):
        ce = self.get_root()
        if ce is None:
            raise ValueError("No Master Protocol.")
        entities = [ce]
        output = []
        cur_level = 0
        while cur_level < level:
            output.clear()
            for entity in entities:
                action = self.get_action_node(entity[0])
                if action is None:
                    output.append(entity)
                    continue
                for act in self.resolve_action(action[0]):
                    output.append(act)
            cur_level += 1
            entities = output.copy()
        return output

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
    
    def get_parent(self,subject):
        subject = self._resolve_subject(subject)
        a_pred = self._model_graph.identifiers.predicates.actions
        c_pred = self._model_graph.identifiers.predicates.has_container
        h_pred = self._model_graph.identifiers.predicates.has_instrument
        w_pred = self._model_graph.identifiers.predicates.well
        parent_ps = [a_pred,c_pred,h_pred,w_pred]
        res = self._graph.search((None,parent_ps,subject),True)
        if res:
            return res[0]

        res = self._graph.search((None,RDF.first,subject),True)
        if not res:
            return None
        while res != []:
            subj = res[0]
            res = self._graph.search((None,RDF.rest,subj),True)

        res = self._graph.search((None,a_pred,subj),True)
        return res[0]

    def get_children(self,subject):
        child_predicates = [self._model_graph.identifiers.predicates.actions,
                            self._model_graph.identifiers.predicates.has_container,
                            self._model_graph.identifiers.predicates.has_instrument,
                            self._model_graph.identifiers.predicates.well]
        return self._graph.search((subject,child_predicates,None))

    def get_object_code(self,uri):
        for n_id,n_data in self.nodes(data=True):
            if uri == n_data["key"]:
                return n_id
        return None


    def build_nv_id(self,name):
        return URIRef(self._model_graph.identifiers.namespaces.nv + name)



