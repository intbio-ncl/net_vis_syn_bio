from builder.builders.abstract_view import AbstractViewBuilder
class ViewBuilder(AbstractViewBuilder):
    def __init__(self,builder):
        super().__init__(builder)

    def full(self):
        return self._builder._graph

    def pruned(self):
        edges = []
        node_attrs = {}
        w_predicates = self._builder._model_graph.identifiers.predicates
        blacklist = [self._builder._model_graph.identifiers.predicates.consistsOf]
        for n,v,k,e in self._builder.edges(keys=True,data=True):
            if k not in w_predicates:
                continue
            if k in blacklist:
                continue
            node_attrs[n] = self._builder.nodes[n]
            node_attrs[v] = self._builder.nodes[v]
            edges.append((n,v,k,e))
        return self._builder.sub_graph(edges,node_attrs)
         
    def hierarchy(self):
        edges = []
        node_attrs = {}
        for entity,data in self._builder.get_entities():
            children = self._builder.get_children(entity)
            if len(children) == 0:
                continue
            node_attrs[entity] = data
            for child,key in children:
                child,c_data = child
                node_attrs[child] = c_data
                edge = self._build_edge_attr(key)
                edges.append((entity,child,key,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def interaction_explicit(self):
        edges = []
        node_attrs = {}
        for interaction,i_type,e in self._builder.get_interaction():
            interaction,interaction_data = interaction
            consistsOf = self._builder.get_consistsof(interaction,True)
            if consistsOf == []:
                raise NotImplementedError("Not Implemented.")
                continue
            consistsOf = consistsOf[1][0]
            consistsOf = self._builder.resolve_list(consistsOf)
            inputs,outputs = self._builder.get_interaction_io(interaction)
            for index,n in enumerate(consistsOf):
                n,n_data = n
                node_attrs[n] = n_data
                if index == len(consistsOf) -1:
                    for obj,pred in outputs:
                        obj,obj_data = obj
                        node_attrs[obj] = obj_data
                        edge = self._build_edge_attr(pred)
                        edges.append((n,obj,pred,edge))
                if index == 0:
                    for obj,pred in inputs:
                        obj,obj_data = obj
                        node_attrs[obj] = obj_data
                        edge = self._build_edge_attr(pred)
                        edges.append((obj,n,pred,edge))
                    continue
                p_element = consistsOf[index-1][0]
                edges.append((p_element,n,pred,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def interaction_verbose(self):
        edges = []
        node_attrs = {}
        for interaction,i_type,e in self._builder.get_interaction():
            interaction,interaction_data = interaction
            inputs,outputs = self._builder.get_interaction_io(interaction)
            for obj,pred in inputs:
                obj,obj_data = obj
                node_attrs[obj] = obj_data
                edge = self._build_edge_attr(pred)
                edges.append((obj,interaction,pred,edge))
            for obj,pred in outputs:
                obj,obj_data = obj
                node_attrs[obj] = obj_data
                edge = self._build_edge_attr(pred)
                edges.append((interaction,obj,pred,edge))
            node_attrs[interaction] = interaction_data
        return self._builder.sub_graph(edges,node_attrs)

    def interaction(self):
        edges = []
        node_attrs = {}
        for interaction,i_type,e in self._builder.get_interaction():
            interaction,interaction_data = interaction
            i_type,i_type_data = i_type
            i_type_key = i_type_data["key"]
            inputs,outputs = self._builder.get_interaction_io(interaction)
            for inp,pred in inputs:
                inp,inp_data = inp
                node_attrs[inp] = inp_data
                for out,pred in outputs:
                    out,out_data = out
                    node_attrs[out] = out_data
                    edge = self._build_edge_attr(i_type_key)
                    edges.append((inp,out,i_type_key,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def interaction_genetic(self):
        genetic_pred = self._builder._model_graph.identifiers.objects.DNA
        return self._produce_interaction_graph(genetic_pred)

    def interaction_protein(self):
        p_pred = self._builder._model_graph.identifiers.objects.protein
        return self._produce_interaction_graph(p_pred,True)

    def interaction_io(self):
        edges = []
        node_attrs = {}
        i_graph = self.interaction()
        for input,outputs in self._get_interaction_io(i_graph):
            i,i_data = input
            node_attrs[i] = i_data
            for o,e in outputs:
                node_attrs[o] = i_graph.nodes[o]
                edge = self._build_edge_attr(e)
                edges.append((i,o,e,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def _get_interaction_io(self,graph):
        inputs = [n for n in graph.nodes(data=True) if len(graph.in_edges(n[0])) == 0]
        io = []
        ends = list(set(self._get_loop_ends(inputs,graph)))
        for inp in inputs:
            for n,v,e in graph.out_edges(inp[0],keys=True):
                io.append((inp,self._get_outputs_inner(v,e,graph,ends)))
        return io

    def _get_outputs_inner(self,subject,predicate,graph,l_ends):
        i_targets = []
        out_edges = graph.out_edges(subject,keys=True)
        if len(out_edges) == 0:
            i_targets.append((subject,predicate))
            return i_targets
        for n1,v1,e1 in out_edges:
            if v1 in l_ends:
                i_targets.append((v1,predicate))
            else:
                i_targets += self._get_outputs_inner(v1,e1,graph,l_ends)
        return i_targets

    def _get_loop_ends(self,inputs,graph):
        l_ends = []
        def _get_target_inner(subject,seens=[]):
            out_edges = graph.out_edges(subject,keys=True)
            for n1,v1,e1 in out_edges:
                if n1 in l_ends:
                    return 
                if v1 in seens:
                    l_ends.append(n1)
                    continue
                else:
                    seens.append(n1)
                    _get_target_inner(v1,seens.copy())
        for n,data in inputs:
            _get_target_inner(n)
        return l_ends

    def _produce_interaction_graph(self,predicate,first_pred=False):
        edges = []
        node_attrs = {}
        i_graph = self.interaction()
        g_code = [self._builder._model_graph.get_class_code(predicate)]
        for n,n_data in i_graph.nodes(data=True):
            n_type = self._builder.get_rdf_type(n)[1]["key"]
            if not self._builder._model_graph.is_derived(n_type,g_code):
                continue
            node_attrs[n] = n_data
            for v,e in self._find_nearest_interaction(n,g_code,i_graph,first_pred):
                node_attrs[v] = i_graph.nodes[v]
                edge = self._build_edge_attr(e)
                edges.append((n,v,e,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def _find_nearest_interaction(self,node,target_types,graph,use_first=False):
        def _find_nearest_inner(c_node,index=0,first_pred=None):
            i_targets = []
            for n,v,e in graph.edges(c_node,keys=True):
                # Self Loops.
                if n == v:
                    continue
                if index == 0 :
                    first_pred = e
                node_type = self._builder.get_rdf_type(v)
                if node_type is None:
                    continue
                node_type = node_type[1]["key"]
                if self._builder._model_graph.is_derived(node_type,target_types):
                    if use_first:
                        e = first_pred
                    i_targets.append((v,e,index))
                    continue
                i_targets += _find_nearest_inner(v,index+1,first_pred)
            return i_targets
            
        targets = _find_nearest_inner(node)
        f_targets = []
        # Remove paths to same object (Remove longest.)
        if len(targets) < 2:
            return [t[:2] for t in targets]
        for index1,(t1,e1,distance1) in enumerate(targets):
            if [t[0] for t in targets].count(t1) == 1:
                f_targets.append((t1,e1))
                continue
            for index2,(t2,e2,distance2) in enumerate(targets):
                if index1 == index2:
                    continue
                if t1 != t2:
                    continue
                if distance2 > distance1:
                    f_targets.append((t1,e1))
                elif distance1 > distance2:
                    f_targets.append((t2,e2))
                else:
                    f_targets.append((t1,e1))
                    f_targets.append((t2,e2))
        return f_targets

