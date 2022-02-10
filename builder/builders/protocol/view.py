from re import L, sub
from typing import Container
from builder.builders.abstract_view import AbstractViewBuilder
from rdflib import URIRef
from rdflib import RDF
from rdflib import BNode

class ViewBuilder(AbstractViewBuilder):
    def __init__(self,builder):
        super().__init__(builder)

    def full(self):
        return self._builder._graph

    def pruned(self):
        edges = []
        node_attrs = {}
        ids = self._builder._model_graph.identifiers
        nv_actions = ids.predicates.actions
        blacklist = [RDF.type,RDF.first,RDF.rest]
        for n,v,k,e in self._builder.edges(keys=True,data=True):
            n_data = self._builder.nodes[n]
            v_data = self._builder.nodes[v]
            if k in blacklist:
                continue
            elif isinstance(n_data["key"],BNode):
                continue
            elif k == nv_actions:
                node_attrs[n] = self._builder.nodes[n]
                actions = self._builder.resolve_action(v)
                p_a = n
                for index,a in enumerate(actions):
                    a,a_data = a
                    k = self._builder.build_nv_id("next-action")
                    edge = self._build_edge_attr(k)
                    edges.append((p_a,a,k,edge))
                    node_attrs[a] = a_data
                    p_a = a
            else:
                node_attrs[n] = self._builder.nodes[n]
                node_attrs[v] = self._builder.nodes[v]
                edges.append((n,v,k,e))
        return self._builder.sub_graph(edges,node_attrs)

    def hierarchy(self):
        edges = []
        node_attrs = {}
        ids = self._builder._model_graph.identifiers
        nv_protocol = ids.objects.protocol
        nv_has_container = ids.predicates.has_container
        nv_actions = ids.predicates.actions
        for c_id,c_data in [c[0] for c in self._builder.get_container()]:
            node_attrs[c_id] = c_data
            parent = self._builder.get_parent(c_id)
            assert(parent)
            p_id,p_data = parent
            p_t_id,p_t_data = self._builder.get_rdf_type(p_id)
            if p_t_data["key"] == nv_protocol:
                continue
            node_attrs[p_id] = p_data
            edge = self._build_edge_attr(nv_has_container)
            edges.append((p_id,c_id,nv_has_container,edge))

        for n,v,e in self._builder.get_actions():
            n_id,n_data = n
            v_id,v_data = v
            
            n_t_id,n_t_data = self._builder.get_rdf_type(n_id)
            if n_t_data["key"] == nv_protocol:
                continue
            node_attrs[n_id] = n_data
            for a_id,a_data in self._builder.resolve_action(v_id):
                node_attrs[a_id] = a_data
                edge = self._build_edge_attr(nv_actions)
                edges.append((n_id,a_id,nv_actions,edge))

        return self._builder.sub_graph(edges,node_attrs)

    def instructions(self,level,detail):
        edges = []
        node_attrs = {}
        node_attrs = {}
        nv_source = self._builder._model_graph.identifiers.predicates.source
        nv_dest = self._builder._model_graph.identifiers.predicates.destination

        actions = self._builder.get_abstraction_level(level)
        for index,(a_id,a_data) in enumerate(actions):
            node_attrs[a_id] = a_data
            if detail:
                inputs,outputs = self._builder.get_io(a_id)
                for inp,inp_data in inputs:
                    if self._is_internal_action(inp,a_id,actions):
                        continue
                    node_attrs[inp] = inp_data
                    edge = self._build_edge_attr(nv_source)
                    edges.append((inp,a_id,nv_source,edge))
                for out,out_data in outputs:
                    if self._is_internal_action(out,a_id,actions):
                        continue
                    node_attrs[out] = out_data
                    edge = self._build_edge_attr(nv_dest)
                    edges.append((a_id,out,nv_dest,edge))
            if index >= len(actions)-1:
                continue
            next_action = actions[index+1][0]
            k = self._builder.build_nv_id("next-action")
            edge = self._build_edge_attr(k)
            edges.append((a_id,next_action,k,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def flow(self,level,detail):
        edges = []
        node_attrs = {}
        nv_source = self._builder._model_graph.identifiers.predicates.source
        nv_dest = self._builder._model_graph.identifiers.predicates.destination
        actions = self._builder.get_abstraction_level(level)
        seens = []
        def _add_well(i_action,o_action,well,direction):
            if o_action not in actions:
                o_action = self._find_parent_action(o_action[0],actions)
            o_action,o_action_data = o_action
            well,well_data = well
            node_attrs[o_action] = o_action_data
            if o_action == well:
                return False
            if i_action == o_action:
                return False
            if direction == nv_source:
                edge = (i_action,o_action,well_data["key"])
                if edge in seens:
                    return False
                seens.append(edge)
                edge = (*edge,self._build_edge_attr(well_data["key"]))
                edges.append(edge)
                return True
            elif direction == nv_dest and detail:
                edge = (o_action,i_action,well_data["key"])
                if edge in seens:
                    return False
                seens.append(edge)
                edge = (*edge,self._build_edge_attr(well_data["key"]))
                edges.append(edge)
                return True
            return False

        prev_actions = []
        for index,action in enumerate(actions):
            a_id,a_data = action
            node_attrs[a_id] = a_data
            wells = self._builder.get_wells(a_id,True)
            if len(wells) == 0:
                for p_well,p_dir in prev_actions:
                    _add_well(actions[index-1][0],action,p_well,p_dir)
            pa = []
            for well in wells:
                wa = self._builder.get_well_actions(well)
                for n1,v1,e1 in wa:
                    if _add_well(a_id,n1,well,e1):
                        pa.append((well,e1))
            if pa != []:
                prev_actions = pa
        return self._builder.sub_graph(edges,node_attrs)

    def io(self,level,detail):
        edges = []
        node_attrs = {}
        actions = self._builder.get_abstraction_level(level)
        nv_source = self._builder._model_graph.identifiers.predicates.source
        nv_dest = self._builder._model_graph.identifiers.predicates.destination
        for a_id,a_data in actions:
            node_attrs[a_id] = a_data
            inputs,outputs = self._builder.get_io(a_id,detail)
            for i_id,i_data in inputs:
                node_attrs[i_id] = i_data
                edge = self._build_edge_attr(nv_source)
                edges.append((i_id,a_id,nv_source,edge))

            for o_id,o_data in outputs:
                node_attrs[o_id] = o_data
                edge = self._build_edge_attr(nv_dest)
                edges.append((a_id,o_id,nv_dest,edge))

        graph = self._builder.sub_graph(edges,node_attrs)
        graph = self._prune_edges(graph)
        graph = self._reattach(graph,actions)
        return graph

    def process(self,level,detail):
        edges = []
        node_attrs = {}
        prev_output = []
        actions = self._builder.get_abstraction_level(level)
        for index,(a_id,a_data) in enumerate(actions):
            inputs,outputs = self._builder.get_io(a_id,False)
            outputs = [o for o in outputs if not self._is_internal_action(o[0],a_id,actions[index:])]
            inputs = [i for i in inputs if not self._is_internal_action(i[0],a_id,actions)]
            if len(inputs) == 0 and index > 0 and detail:
                inputs = prev_output
            if len(outputs) == 0 and index > 0:
                outputs = prev_output

            for inp in inputs:
                i_id,i_data = inp
                for o_id,o_data in outputs:
                    node_attrs[i_id] = i_data
                    node_attrs[o_id] = o_data
                    edge = self._build_edge_attr(a_data["key"])
                    edges.append((i_id,o_id,a_data["key"],edge))
            prev_output = outputs
        return self._builder.sub_graph(edges,node_attrs)

    def container(self,level):
        edges = []
        node_attrs = {}
        for n,v,e in self._builder.get_proto_actions():
            n,n_data = n
            node_attrs[n] = n_data
            for n1,v1,e1 in self._builder.get_containers(n):
                v1,v1_data = v1
                node_attrs[v1] = v1_data
                edge = self._build_edge_attr(e1)
                edges.append((n,v1,e1,edge)) 
        return self._builder.sub_graph(edges,node_attrs)

    def _prune_edges(self,graph):
        '''
        For certain abstraction levels internal actions are superflous for visualisation.
        This attempts to remove some of these.
        '''
        nv_dest = self._builder._model_graph.identifiers.predicates.destination
        nv_source = self._builder._model_graph.identifiers.predicates.source
        edges = list(graph.edges(keys=True))
        for n,v,e in edges:
            if e == nv_dest:
                inter_loop = [(v,n,nv_source),(n,v,nv_dest)]
                in_edges = list(graph.in_edges(v,keys=True))
                out_edges = list(graph.out_edges(v,keys=True))
                edges = in_edges + out_edges
                if set(inter_loop) == set(edges):
                    graph.remove_node(v)
                    continue
        return graph

    def _reattach(self,graph,actions):
        '''
        Some Actions and Protocols may have no inputs or outputs. 
        '''
        nv_dest = self._builder._model_graph.identifiers.predicates.destination
        nv_source = self._builder._model_graph.identifiers.predicates.source
        for index,(a,a_data) in enumerate(actions):
            edges = list(graph.in_edges(a,keys=True)) + list(graph.out_edges(a,keys=True))
            sources = [e for e in edges if e[2] == nv_source]
            dests = [e for e in edges if e[2] == nv_dest]
            if len(sources) == 0 and index != 0:
                prev_action = actions[index-1]
                pa_outputs = graph.out_edges(prev_action[0],keys=True)
                sources = [(a[1],graph.nodes[a[1]]) for a in pa_outputs]
                for source in sources:
                    graph.add_edge(source[0],a,nv_source)
            if len(dests) == 0:
                for source in sources:
                    in_edges = list(graph.in_edges(source[0],keys=True))
                    for n,v,e in in_edges:
                        graph.add_edge(a,v,e)
        return graph

    def _add_action_properties(self,action_id,edges,node_attrs):
        for n,v,e in self._builder.get_properties(action_id):
            node_attrs[v[0]] = v[1]
            edge = self._build_edge_attr(e)
            edges.append((n[0],v[0],e,edge))
        return edges,node_attrs

    def _find_parent_action(self,subject,actions):
        parent = self._builder.get_parent(subject)
        if subject == 0:
            return [None]
        if parent in actions:
            return parent
        return self._find_parent_action(parent[0],actions)

    def _is_internal_action(self,subject,action,actions):
        nv_dest = self._builder._model_graph.identifiers.predicates.destination
        well_actions = self._builder.get_well_actions(subject)
        if nv_dest not in [w[2] for w in well_actions]:
            # Input only Nodes
            return False
        for n,v,e in well_actions:
            if n in actions and n != action:
                return False
            pa = self._find_parent_action(n[0],actions)
            if pa[0] and pa[0] != action:
                return False
        return True